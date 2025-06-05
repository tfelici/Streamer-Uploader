# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for macOS standalone executable
Creates a single-file executable with all dependencies bundled
"""

import sys
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Add the parent directory to the path so we can import from main.py
sys.path.insert(0, os.path.abspath('..'))

# Collect data files for templates and static content
template_files = collect_data_files('templates', include_py_files=False)
static_files = collect_data_files('static', include_py_files=False)

# Add our template and static files manually since they're in parent directory
datas = []
datas.append(('../templates/index.html', 'templates'))
datas.append(('../static/style.css', 'static'))

# Collect all webview submodules
webview_modules = collect_submodules('webview')

a = Analysis(
    ['../main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'webview',
        'webview.platforms.cocoa',
        'webview.platforms.qt',
        'webview.platforms.cef',
        'flask',
        'flask.templating',
        'jinja2',
        'jinja2.ext',
        'werkzeug',
        'werkzeug.serving',
        'requests',
        'requests.adapters',
        'requests.packages',
        'requests.packages.urllib3',
        'requests.packages.urllib3.util',
        'requests.packages.urllib3.util.retry',
        'requests_toolbelt',
        'requests_toolbelt.multipart',
        'requests_toolbelt.multipart.encoder',
        'pymediainfo',
        'utils',
        'json',
        'threading',
        'time',
        'os',
        'sys',
        'subprocess',
        'objc',
        'Foundation',
        'AppKit',
        'WebKit'
    ] + webview_modules,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='EncoderUploader',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
