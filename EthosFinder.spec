# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for ETHOS FINDER
For advanced build customization
"""

block_cipher = None

# Analyze the main script
a = Analysis(
    ['ethos_gui.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('tools', 'tools'),  # Include tools directory
    ],
    hiddenimports=[
        'phonenumbers',
        'requests',
        'cryptography',
        'cryptography.fernet',
        'cryptography.hazmat.primitives',
        'cryptography.hazmat.primitives.kdf.pbkdf2',
        'tkinter',
        'tkinter.ttk',
        'tkinter.scrolledtext',
        'tkinter.messagebox',
        'tkinter.filedialog',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Create the PYZ archive
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Build the executable
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='EthosFinder',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Use UPX compression
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to True for console version
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add path to .ico file if available
)
