#!/usr/bin/env python3
"""
Build script for creating ETHOS FINDER executable
Uses PyInstaller to create standalone executable
"""

import os
import sys
import subprocess
import shutil

def check_requirements():
    """Check if required packages are installed."""
    print("[*] Checking requirements...")

    required = ['PyInstaller', 'requests', 'phonenumbers']
    missing = []

    for package in required:
        try:
            __import__(package.lower())
            print(f"  ✓ {package} installed")
        except ImportError:
            print(f"  ✗ {package} NOT installed")
            missing.append(package)

    if missing:
        print(f"\n[!] Missing packages: {', '.join(missing)}")
        print(f"[i] Install with: pip install {' '.join(missing)}")
        return False

    print("[✓] All requirements satisfied\n")
    return True

def clean_build():
    """Clean previous build artifacts."""
    print("[*] Cleaning previous build artifacts...")

    dirs_to_remove = ['build', 'dist', '__pycache__']
    files_to_remove = ['ethos_gui.spec']

    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"  ✓ Removed {dir_name}/")

    for file_name in files_to_remove:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"  ✓ Removed {file_name}")

    print("[✓] Clean complete\n")

def build_executable():
    """Build the executable using PyInstaller."""
    print("[*] Building executable...\n")

    # PyInstaller command
    cmd = [
        'pyinstaller',
        '--name=EthosFinder',
        '--onefile',
        '--windowed',  # No console window (GUI only)
        '--icon=NONE',  # Add icon file path if you have one
        '--add-data=tools;tools',  # Include tools directory
        '--hidden-import=phonenumbers',
        '--hidden-import=requests',
        '--hidden-import=cryptography',
        '--hidden-import=tkinter',
        '--clean',
        'ethos_gui.py'
    ]

    # Alternative command for console version (shows debug output)
    cmd_console = cmd.copy()
    cmd_console[3] = '--console'

    try:
        # Ask user which version to build
        print("Build options:")
        print("1) GUI only (no console) - Recommended for distribution")
        print("2) GUI + Console (shows debug output) - Recommended for testing")
        print("3) Both versions")

        choice = input("\nSelect option [1/2/3]: ").strip()

        if choice == "1":
            subprocess.run(cmd, check=True)
        elif choice == "2":
            subprocess.run(cmd_console, check=True)
        elif choice == "3":
            print("\n[*] Building GUI-only version...")
            subprocess.run(cmd, check=True)
            print("\n[*] Building GUI+Console version...")
            # Rename first build
            if os.path.exists('dist/EthosFinder.exe'):
                os.rename('dist/EthosFinder.exe', 'dist/EthosFinder_GUI.exe')
            subprocess.run(cmd_console, check=True)
            if os.path.exists('dist/EthosFinder.exe'):
                os.rename('dist/EthosFinder.exe', 'dist/EthosFinder_Console.exe')
        else:
            print("[!] Invalid choice. Exiting.")
            return False

        print("\n[✓] Build complete!")
        return True

    except subprocess.CalledProcessError as e:
        print(f"\n[!] Build failed: {e}")
        return False
    except Exception as e:
        print(f"\n[!] Unexpected error: {e}")
        return False

def create_readme():
    """Create README for distribution."""
    readme_content = """
ETHOS FINDER v2 - Executable Distribution
==========================================

QUICK START:
1. Run EthosFinder.exe
2. Select search type (Email, Phone, Username)
3. Enter search query and click Search

CONFIGURATION:
- Use Settings → Configure API Keys to add RapidAPI keys
- For maximum security, set environment variable: ETHOS_RAPIDAPI_KEY
- Config stored in config.json (created on first run)

SECURITY:
- API keys are encrypted when stored
- Never share your config.json or .ethos_key files
- This tool is for defensive security and OSINT research only

REQUIREMENTS:
- Windows 10 or later (64-bit)
- Internet connection for searches
- No additional software required

TROUBLESHOOTING:
- If antivirus flags the executable, add an exception
  (This is common with PyInstaller executables)
- Run the Console version for debug output
- Check firewall settings if searches fail

For more information, see documentation in the Help menu.

© 2025 - For educational and defensive security purposes only
"""

    with open('dist/README.txt', 'w') as f:
        f.write(readme_content)

    print("[✓] Created README.txt in dist/")

def main():
    """Main build process."""
    print("="*60)
    print("  ETHOS FINDER - Executable Builder")
    print("="*60 + "\n")

    # Check requirements
    if not check_requirements():
        print("\n[!] Please install missing requirements and try again.")
        sys.exit(1)

    # Clean previous builds
    clean_build()

    # Build executable
    if not build_executable():
        print("\n[!] Build process failed.")
        sys.exit(1)

    # Create distribution files
    create_readme()

    # Summary
    print("\n" + "="*60)
    print("  BUILD SUMMARY")
    print("="*60)
    print(f"\n✓ Executable(s) created in: {os.path.abspath('dist')}/")
    print("\nDistribution contents:")
    if os.path.exists('dist'):
        for item in os.listdir('dist'):
            size = os.path.getsize(os.path.join('dist', item))
            size_mb = size / (1024 * 1024)
            print(f"  - {item} ({size_mb:.2f} MB)")

    print("\n[✓] Build complete! Your executable is ready for distribution.")
    print("\n[i] Note: First run may take a few seconds while extracting.")
    print("[i] Distribute the entire 'dist' folder or just the .exe file.")
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Build cancelled by user.")
        sys.exit(1)
