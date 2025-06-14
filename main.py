#!/usr/bin/env python3
"""
Streamer Uploader - Standalone Upload Recordings App with Integrated Viewer
Replicates only the "Upload Recordings" panel from RPI Streamer app.py
"""

import webview
import threading
import time
import sys
import os
import socket
from flask import Flask, render_template, request, jsonify, Response
import json
import re
from datetime import datetime
from werkzeug.utils import secure_filename
import requests
import uuid
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor

# Use pymediainfo for fast video duration extraction
try:
    from pymediainfo import MediaInfo
except ImportError:
    MediaInfo = None

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils import safe_remove_file

app = Flask(__name__)

# Global dictionary to track upload progress and allow cancellation
upload_progress = {}
upload_threads = {}
# SSE clients tracking for upload progress
upload_sse_clients = {}

# Configuration
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # Running as script
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

STREAMER_DATA_DIR = os.path.join(BASE_DIR, 'streamerData')
RECORDINGS_DIR = os.path.join(STREAMER_DATA_DIR, 'recordings', 'broadcast')
SETTINGS_FILE = os.path.join(STREAMER_DATA_DIR, 'settings.json')

# Create directories if they don't exist
os.makedirs(STREAMER_DATA_DIR, exist_ok=True)
os.makedirs(RECORDINGS_DIR, exist_ok=True)

def load_settings():
    """Load settings from JSON file"""
    settings = {
        "upload_url": ""
    }
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r') as f:
                settings.update(json.load(f))
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error loading settings: {e}")
    return settings

def save_settings(settings):
    """Save settings to JSON file"""
    try:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving settings: {e}")
        return False

def get_video_duration_mediainfo(path):
    """Get video duration using pymediainfo library"""
    if MediaInfo is None:
        return None
    try:
        media_info = MediaInfo.parse(path)
        for track in media_info.tracks:
            if track.track_type == 'Video' and track.duration:
                return track.duration / 1000.0  # ms to seconds
        # fallback: try general track
        for track in media_info.tracks:
            if track.track_type == 'General' and track.duration:
                return track.duration / 1000.0
    except Exception:
        pass
    return None

def get_recording_files():
    """Get list of recording files from the recordings directory"""
    files = []
    if os.path.exists(RECORDINGS_DIR):
        file_list = [f for f in os.listdir(RECORDINGS_DIR) if f.endswith('.mp4')]
        # Sort by modification time, newest first
        file_list.sort(key=lambda f: os.path.getmtime(os.path.join(RECORDINGS_DIR, f)), reverse=True)
        
        for filename in file_list:
            file_path = os.path.join(RECORDINGS_DIR, filename)
            try:
                size = os.path.getsize(file_path)
                duration = get_video_duration_mediainfo(file_path)
                
                # Extract timestamp from filename if possible (format: timestamp.mp4)
                m = re.match(r'^(\d+)\.mp4$', filename)
                timestamp = int(m.group(1)) if m else None
                
                files.append({
                    'path': file_path,
                    'name': filename,
                    'size': size,
                    'location': 'Local',
                    'active': False,  # No active recordings in uploader
                    'duration': duration,
                    'timestamp': timestamp
                })
            except OSError:
                continue
    return files

@app.template_filter('datetimeformat')
def datetimeformat(value):
    """Format timestamp for display"""
    if value is None:
        return ""
    try:
        dt = datetime.fromtimestamp(int(value))
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except:
        return str(value)

@app.template_filter('durationformat')
def durationformat(value):
    """Format duration for display"""
    if value is None:
        return ""
    try:
        seconds = float(value)
        seconds = int(round(seconds))
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60
        if h > 0:
            return f"{h}:{m:02}:{s:02}"
        else:
            return f"{m}:{s:02}"
    except:
        return str(value)

@app.template_filter('filesizeformat')
def filesizeformat(num_bytes):
    """Format file size for display"""
    if num_bytes is None:
        return ""
    try:
        for unit in ['B', 'KB', 'MB', 'GB']:
            if num_bytes < 1024.0:
                return f"{num_bytes:.1f} {unit}"
            num_bytes /= 1024.0
        return f"{num_bytes:.1f} TB"
    except:
        return str(num_bytes)

@app.route('/')
def index():
    """Main page - Upload Recordings only"""
    recording_files = get_recording_files()
    return render_template('index.html', 
                         recording_files=recording_files,
                         streaming=False,
                         uploadrecordingsonly=True)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    """Handle settings"""
    if request.method == 'POST':
        data = request.get_json()
        if data:
            settings = load_settings()
            settings.update(data)
            if save_settings(settings):
                return jsonify({'success': True})
            else:
                return jsonify({'error': 'Failed to save settings'}), 500
        return jsonify({'error': 'No data provided'}), 400
    else:
        return jsonify(load_settings())

@app.route('/upload-recording', methods=['POST'])
def upload_recording():
    """Upload a recording file to the configured server"""
    from werkzeug.utils import secure_filename
    
    settings = load_settings()
    upload_url = settings.get('upload_url', '').strip()
    if not upload_url:
        return jsonify({'error': 'Upload URL is not set. Please configure it in Settings.'}), 400
    
    # Ensure command=replacerecordings is present
    if 'command=replacerecordings' not in upload_url:
        if '?' in upload_url:
            upload_url += '&command=replacerecordings'
        else:
            upload_url += '?command=replacerecordings'
    
    file_path = request.form.get('file_path')
    if not file_path or not os.path.isfile(file_path):
        return jsonify({'error': 'Recording file not found.'}), 400
    
    # Generate unique upload ID for progress tracking
    upload_id = str(uuid.uuid4())
    
    # Store upload progress globally
    upload_progress[upload_id] = {
        'progress': 0,
        'status': 'starting',
        'error': None,
        'result': None,
        'cancelled': False
    }
    
    def upload_file_async():
        try:
            upload_progress[upload_id]['status'] = 'uploading'
            
            # Get file size for progress calculation
            file_size = os.path.getsize(file_path)
            
            def progress_callback(monitor):
                if upload_progress[upload_id]['cancelled']:
                    # Cancel the upload by raising an exception
                    raise Exception("Upload cancelled by user")
                
                progress = min(100, int((monitor.bytes_read / file_size) * 100))
                upload_progress[upload_id]['progress'] = progress
                
                # Notify all SSE clients about the progress
                for client_id, client_data in upload_sse_clients.items():
                    if client_data['upload_id'] == upload_id:
                        try:
                            # Send progress update to SSE client
                            client_data['queue'].put({'progress': progress})
                        except Exception:
                            pass  # Ignore errors in notifying clients
            
            # Use MultipartEncoder for upload with progress monitoring
            with open(file_path, 'rb') as f:
                multipart_data = MultipartEncoder(
                    fields={'video': (secure_filename(os.path.basename(file_path)), f, 'application/octet-stream')}
                )
                
                monitor = MultipartEncoderMonitor(multipart_data, progress_callback)
                
                response = requests.post(
                    upload_url, 
                    data=monitor,
                    headers={'Content-Type': monitor.content_type},
                    timeout=300
                )
                
                if response.status_code == 200:
                    try:
                        result = response.json()
                    except:
                        result = {'success': True, 'message': 'Upload completed', 'error': ''}
                else:
                    result = {'error': f'Upload failed: {response.status_code}'}
                
                upload_progress[upload_id]['status'] = 'completed'
                upload_progress[upload_id]['progress'] = 100
                upload_progress[upload_id]['result'] = result                # If upload succeeded and no error, delete the original file
                if result.get('error') == '':
                    try:
                        safe_remove_file(file_path)
                    except Exception:
                        pass  # Ignore deletion errors
                        
        except Exception as e:
            if upload_progress[upload_id]['cancelled']:
                upload_progress[upload_id]['status'] = 'cancelled'
                upload_progress[upload_id]['error'] = 'Upload cancelled by user'
            else:
                upload_progress[upload_id]['status'] = 'error'
                upload_progress[upload_id]['error'] = f'Upload failed: {e}'
        finally:
            # Clean up thread reference
            if upload_id in upload_threads:
                del upload_threads[upload_id]
    
    # Start upload in background thread
    thread = threading.Thread(target=upload_file_async)
    thread.daemon = True
    thread.start()
    
    # Store thread reference for potential cancellation
    upload_threads[upload_id] = thread
    
    return jsonify({'upload_id': upload_id, 'status': 'started'})

@app.route('/upload-progress/<upload_id>')
def get_upload_progress(upload_id):
    """Get the current progress of an upload"""
    if upload_id not in upload_progress:
        return jsonify({'error': 'Upload ID not found'}), 404
    
    progress_data = upload_progress[upload_id].copy()
    
    # Clean up completed/error/cancelled uploads after returning status
    if progress_data['status'] in ['completed', 'error', 'cancelled']:
        # Keep the data for a short time to allow frontend to get final status
        pass
    
    return jsonify(progress_data)

@app.route('/cancel-upload/<upload_id>', methods=['POST'])
def cancel_upload(upload_id):
    """Cancel an ongoing upload"""
    if upload_id not in upload_progress:
        return jsonify({'error': 'Upload ID not found'}), 404
    
    # Mark upload as cancelled
    upload_progress[upload_id]['cancelled'] = True
    upload_progress[upload_id]['status'] = 'cancelling'
    
    return jsonify({'status': 'cancelling'})

@app.route('/upload-progress-stream/<upload_id>')
def upload_progress_stream(upload_id):
    """SSE endpoint for real-time upload progress monitoring"""
    def generate():
        # Send initial connection event
        yield f"data: {json.dumps({'type': 'connected', 'upload_id': upload_id})}\n\n"
        
        # Monitor upload progress
        while upload_id in upload_progress:
            progress_data = upload_progress[upload_id].copy()
            
            # Send progress update
            progress_data['type'] = 'progress'
            yield f"data: {json.dumps(progress_data)}\n\n"
            
            # If upload is finished, send final status and close
            if progress_data['status'] in ['completed', 'error', 'cancelled']:
                time.sleep(0.1)  # Small delay to ensure client receives final update
                break
                
            time.sleep(0.2)  # Update every 200ms for real-time feel
        
        # Send close event
        yield f"data: {json.dumps({'type': 'closed', 'upload_id': upload_id})}\n\n"
    
    return Response(
        generate(),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Cache-Control'
        }
    )

@app.route('/delete-recording', methods=['POST'])
def delete_recording():
    """Delete a recording file"""
    data = request.get_json()
    file_path = data.get('file_path')
    if not file_path or not os.path.isfile(file_path):
        return jsonify({'error': 'Recording file not found.'}), 400
    try:
        if safe_remove_file(file_path):
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Failed to delete file'}), 500
    except Exception as e:
        return jsonify({'error': f'Failed to delete: {e}'}), 500

# Web viewer functions
def is_port_available(port):
    """Check if a port is available"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', port))
            return True
    except OSError:
        return False

def find_available_port(start_port=5000, max_port=5100):
    """Find an available port"""
    for port in range(start_port, max_port):
        if is_port_available(port):
            return port
    return None

def start_flask_server(port):
    """Start Flask server in a separate thread"""
    app.run(host='127.0.0.1', port=port, debug=False, use_reloader=False)

def main():
    """Main function to start the application"""
    print("Starting Streamer Uploader...")
    
    # Find available port
    port = find_available_port()
    if not port:
        print("No available ports found!")
        return
    
    print(f"Starting server on port {port}...")
    
    # Start Flask server in background thread
    server_thread = threading.Thread(target=start_flask_server, args=(port,))
    server_thread.daemon = True
    server_thread.start()
    
    # Wait a moment for server to start
    time.sleep(2)
    
    # Create webview window
    window_title = "Streamer Uploader"
    window_url = f"http://127.0.0.1:{port}"
    
    print(f"Opening web viewer: {window_url}")
    # Create and start webview
    webview.create_window(
        window_title, 
        window_url,
        width=1000,
        height=700,
        resizable=True
    )
    
    webview.start(debug=False)

if __name__ == '__main__':
    main()
