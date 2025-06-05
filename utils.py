#!/usr/bin/env python3
"""
Utility functions for Streamer Uploader
"""

import os


def safe_remove_file(file_path):
    """
    Safely remove a file and ensure it's actually deleted from storage device.
    This function handles proper filesystem syncing to prevent issues with USB drives
    where files appear deleted but are still present when the device is reinserted.
    
    Args:
        file_path (str): Path to the file to be removed
        
    Returns:
        bool: True if file was successfully removed, False otherwise
    """
    try:
        os.remove(file_path)
        
        # Force filesystem sync to ensure deletion is written to disk
        try:
            if os.name == 'nt':  # Windows
                import ctypes
                # Get the drive letter of the file path
                drive = os.path.splitdrive(file_path)[0]
                if drive:
                    # Force flush of all cached writes for this drive
                    handle = ctypes.windll.kernel32.CreateFileW(
                        drive + "\\", 0x40000000, 3, None, 3, 0x02000000, None
                    )
                    if handle != -1:
                        ctypes.windll.kernel32.FlushFileBuffers(handle)
                        ctypes.windll.kernel32.CloseHandle(handle)
            else:  # Unix-like systems
                os.sync()
        except Exception:
            pass  # Ignore sync errors
            
        return True
    except Exception as e:
        print(f"Error removing file {file_path}: {e}")
        return False