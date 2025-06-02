#!/usr/bin/env python3
"""
Encoder Uploader - Standalone Upload Recordings App with Integrated Viewer
Replicates only the "Upload Recordings" panel from RPI Encoder app.py
"""

import webview
import threading
import time
import sys
import os
import socket
from flask import Flask, render_template, request, jsonify
import json
import re
from datetime import datetime
from werkzeug.utils import secure_filename
import requests

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)

# Configuration
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # Running as script
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ENCODER_DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, 'encoderData'))
SETTINGS_FILE = os.path.join(ENCODER_DATA_DIR, 'settings.json')

# Ensure encoderData directory exists
os.makedirs(ENCODER_DATA_DIR, exist_ok=True)
os.makedirs(os.path.join(ENCODER_DATA_DIR, 'recordings', 'broadcast'), exist_ok=True)

def find_available_port(start_port=5000, max_attempts=10):
    """Find an available port starting from start_port"""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('127.0.0.1', port))
                return port
        except OSError:
            continue
    raise RuntimeError(f"Could not find available port in range {start_port}-{start_port + max_attempts}")

# Global variable to store the selected port
FLASK_PORT = None

def load_settings():
    """Load settings from settings.json"""
    settings = {
        "upload_url": ""
    }
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r') as f:
                settings.update(json.load(f))
        except Exception as e:
            print(f"Error loading settings: {e}")
    return settings

def save_settings(settings):
    """Save settings to settings.json"""
    try:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f)
    except Exception as e:
        print(f"Error saving settings: {e}")

# Jinja2 filter to format UNIX timestamp as human-readable date/time
@app.template_filter('datetimeformat')
def datetimeformat_filter(value):
    try:
        return datetime.utcfromtimestamp(int(value)).strftime('%Y-%m-%d %H:%M:%S UTC')
    except Exception:
        return str(value)

# Jinja2 filter to format seconds as H:MM:SS or MM:SS
@app.template_filter('durationformat')
def durationformat_filter(value):
    try:
        seconds = float(value)
        seconds = int(round(seconds))
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60
        if h > 0:
            return f"{h}:{m:02d}:{s:02d}"
        else:
            return f"{m}:{s:02d}"
    except Exception:
        return str(value)

# Jinja2 filter to format file size in MB
@app.template_filter('filesizeformat')
def filesizeformat_filter(value):
    try:
        size_bytes = int(value)
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"
    except Exception:
        return str(value)

# Jinja2 filter to parse recording filename
@app.template_filter('parse_recording_filename')
def parse_recording_filename_filter(filename):
    try:
        basename = os.path.basename(filename)
        # Pattern: timestamp + 'd' + duration + '.mp4'
        match = re.search(r'(\d+)d([\d.]+)\.mp4$', basename)
        if match:
            timestamp = int(match.group(1))
            duration = float(match.group(2))
            return {
                'timestamp': timestamp,
                'duration': duration
            }
    except Exception:
        pass
    return None

def add_files_from_path(path, file_list, active_files=None):
    """Add files from a given path to the file list"""
    if active_files is None:
        active_files = set()
    
    if not os.path.exists(path):
        return
    
    for filename in os.listdir(path):
        if filename.endswith('.mp4'):
            file_path = os.path.join(path, filename)
            file_size = os.path.getsize(file_path)
            file_list.append({
                'path': file_path,
                'size': file_size,
                'active': filename in active_files
            })

@app.route('/')
def index():
    # Get recording files
    recording_files = []
    recordings_path = os.path.join(ENCODER_DATA_DIR, 'recordings', 'broadcast')
    add_files_from_path(recordings_path, recording_files)
    
    # Sort by modification time (newest first)
    recording_files.sort(key=lambda x: os.path.getmtime(x['path']), reverse=True)
    
    return render_template('index.html', recording_files=recording_files)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        data = request.get_json()
        if data:
            save_settings(data)
            return jsonify({'success': True})
        return jsonify({'error': 'No data provided'}), 400
    else:
        return jsonify(load_settings())

@app.route('/upload-recording', methods=['POST'])
def upload_recording():
    file_path = request.form.get('file_path')
    if not file_path or not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 400
    
    settings = load_settings()
    upload_url = settings.get('upload_url')
    if not upload_url:
        return jsonify({'error': 'Upload URL not configured'}), 400    # Ensure command=replacerecordings is present
    if 'command=replacerecordings' not in upload_url:
        if '?' in upload_url:
            upload_url += '&command=replacerecordings'
        else:
            upload_url += '?command=replacerecordings'
    
    try:
        with open(file_path, 'rb') as file:
            files = {'video': (secure_filename(os.path.basename(file_path)), file)}
            response = requests.post(upload_url, files=files, timeout=300)
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    return jsonify(result)
                except:
                    return jsonify({'success': True, 'message': 'Upload completed'})
            else:
                return jsonify({'error': f'Upload failed: {response.status_code}'}), 500
                
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/delete-recording', methods=['POST'])
def delete_recording():
    data = request.get_json()
    file_path = data.get('file_path')
    
    if not file_path or not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 400
    
    try:
        os.remove(file_path)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def start_flask_app():
    """Start Flask app in a separate thread"""
    global FLASK_PORT
    app.run(host='127.0.0.1', port=FLASK_PORT, debug=False, use_reloader=False)

def main():
    """Main function to start the application"""
    global FLASK_PORT
    
    # Find an available port
    try:
        FLASK_PORT = find_available_port()
        print(f"Starting Flask server on port {FLASK_PORT}")
    except RuntimeError as e:
        print(f"Error: {e}")
        return
    
    # Start Flask in a separate thread
    flask_thread = threading.Thread(target=start_flask_app, daemon=True)
    flask_thread.start()
    
    # Wait a moment for Flask to start
    time.sleep(2)
    
    # Create the webview window with dynamic URL
    webview.create_window(
        'Encoder Uploader',
        f'http://127.0.0.1:{FLASK_PORT}',
        width=1000,
        height=700,
        resizable=True,
        min_size=(800, 600)
    )
    
    # Start the webview
    webview.start(debug=False)

if __name__ == '__main__':
    main()
