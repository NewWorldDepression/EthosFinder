# ETHOS FINDER - Build Guide

Complete guide for building ETHOS FINDER into a standalone executable.

---

## Prerequisites

### 1. Python Installation
- Python 3.8 or later (3.10+ recommended)
- Download from: https://www.python.org/downloads/

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

This will install:
- `phonenumbers` - Phone number parsing
- `requests` - HTTP requests
- `cryptography` - Secure API key storage
- `pyinstaller` - Executable builder

---

## Quick Build (Automated)

### Method 1: Using Build Script (Recommended)

```bash
python build_executable.py
```

The script will:
1. Check all requirements
2. Clean previous builds
3. Ask which version to build (GUI-only, Console, or Both)
4. Create the executable in `dist/` folder
5. Generate README for distribution

**Build Options:**
- **Option 1**: GUI only (no console) - Best for distribution
- **Option 2**: GUI + Console - Best for debugging
- **Option 3**: Both versions

---

## Manual Build (Advanced)

### Using PyInstaller Directly

#### Basic Build (Console Version)
```bash
pyinstaller --onefile --name=EthosFinder ethos_gui.py
```

#### GUI-Only Build (No Console)
```bash
pyinstaller --onefile --windowed --name=EthosFinder ethos_gui.py
```

#### Advanced Build (Using Spec File)
```bash
pyinstaller EthosFinder.spec
```

### Custom Build Options

```bash
pyinstaller ^
  --name=EthosFinder ^
  --onefile ^
  --windowed ^
  --icon=icon.ico ^
  --add-data="tools;tools" ^
  --hidden-import=phonenumbers ^
  --hidden-import=cryptography ^
  --hidden-import=requests ^
  --clean ^
  ethos_gui.py
```

**Options explained:**
- `--onefile` - Single executable file
- `--windowed` - No console window (GUI only)
- `--icon` - Custom icon (provide .ico file)
- `--add-data` - Include additional files/folders
- `--hidden-import` - Explicitly include modules
- `--clean` - Clean cache before building

---

## Build Output

After successful build, you'll find:

```
dist/
├── EthosFinder.exe         # Main executable
└── README.txt              # Distribution readme
```

**File Size:** Approximately 20-30 MB (includes Python runtime and all dependencies)

---

## Testing the Executable

### 1. Local Testing
```bash
cd dist
EthosFinder.exe
```

### 2. Test Checklist
- ✅ Application launches without errors
- ✅ All tabs are accessible (Email, Phone, Username)
- ✅ Search functionality works
- ✅ Settings menu opens
- ✅ Results display correctly
- ✅ Export function works

### 3. Test on Clean System
- Test on a computer without Python installed
- Ensure all features work standalone

---

## Distribution

### What to Include

**Minimal Distribution:**
```
EthosFinder.exe
```

**Full Distribution:**
```
EthosFinder.exe
README.txt
SECURITY_IMPROVEMENTS.md
LICENSE.txt (if applicable)
```

### Distribution Checklist

- [ ] Test executable on clean Windows 10/11 system
- [ ] Verify antivirus doesn't flag it (see Antivirus section)
- [ ] Include README with usage instructions
- [ ] Remove any test config.json or .ethos_key files
- [ ] Consider code signing (optional, for corporate use)

---

## Common Issues & Solutions

### Issue 1: "Failed to execute script"

**Cause:** Missing dependencies or incorrect paths

**Solution:**
```bash
# Rebuild with verbose output
pyinstaller --onefile --console --name=EthosFinder ethos_gui.py

# Check for error messages
```

### Issue 2: Import Errors

**Cause:** Hidden imports not detected

**Solution:** Add to spec file:
```python
hiddenimports=[
    'phonenumbers',
    'cryptography',
    'requests',
    'tkinter',
]
```

### Issue 3: Tools Directory Not Found

**Cause:** Additional data not included

**Solution:**
```bash
pyinstaller --add-data="tools;tools" ethos_gui.py
```

### Issue 4: Antivirus False Positive

**Cause:** PyInstaller executables sometimes trigger antivirus

**Solutions:**
1. Add exception in antivirus software
2. Submit to antivirus vendor as false positive
3. Use code signing certificate (prevents most false positives)
4. Build on a different machine

**Verification:**
- Upload to VirusTotal (https://www.virustotal.com)
- Most reputable AVs should not flag it

### Issue 5: Large File Size

**Cause:** PyInstaller includes entire Python runtime

**Solutions:**
1. Use UPX compression (included in build script)
2. Exclude unused modules
3. Use `--onefile` instead of `--onedir`

**Size Optimization:**
```bash
pyinstaller --onefile --upx-dir=/path/to/upx ethos_gui.py
```

---

## Platform-Specific Builds

### Windows
```bash
# Windows 10/11 (64-bit)
pyinstaller --onefile --windowed ethos_gui.py
```

### Linux
```bash
# Linux (creates ELF executable)
pyinstaller --onefile ethos_gui.py
```

### macOS
```bash
# macOS (creates .app bundle)
pyinstaller --onefile --windowed --name=EthosFinder ethos_gui.py
```

**Note:** Build on the target OS for best compatibility

---

## Advanced Customization

### Adding an Icon

1. Create or download a .ico file (Windows)
2. Add to build command:
```bash
pyinstaller --icon=ethos_icon.ico ethos_gui.py
```

### Version Information (Windows)

Create `version_info.txt`:
```
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(2, 0, 0, 0),
    prodvers=(2, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo([
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'ETHOS'),
        StringStruct(u'FileDescription', u'ETHOS FINDER v2'),
        StringStruct(u'FileVersion', u'2.0.0.0'),
        StringStruct(u'ProductName', u'ETHOS FINDER'),
        StringStruct(u'ProductVersion', u'2.0.0.0')])
    ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
```

Build with version info:
```bash
pyinstaller --version-file=version_info.txt ethos_gui.py
```

### Code Signing (Windows)

```bash
# Sign the executable (requires code signing certificate)
signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com dist\EthosFinder.exe
```

---

## Build Environment Best Practices

### 1. Clean Virtual Environment
```bash
# Create virtual environment
python -m venv build_env

# Activate
build_env\Scripts\activate  # Windows
source build_env/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Build
python build_executable.py
```

### 2. Reproducible Builds
```bash
# Freeze exact versions
pip freeze > requirements-lock.txt

# Build with exact versions
pip install -r requirements-lock.txt
pyinstaller EthosFinder.spec
```

### 3. Clean Before Build
```bash
# Remove cache
python -m PyInstaller --clean

# Or manually delete
rmdir /s /q build dist __pycache__  # Windows
rm -rf build dist __pycache__        # Linux/Mac
```

---

## Automated Build Pipeline

### Example GitHub Actions Workflow

```yaml
name: Build Executable

on: [push, pull_request]

jobs:
  build-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Build executable
        run: python build_executable.py
      - name: Upload artifact
        uses: actions/upload-artifact@v2
        with:
          name: EthosFinder-Windows
          path: dist/EthosFinder.exe
```

---

## Troubleshooting Checklist

Before opening an issue, check:

- [ ] Python version 3.8+ installed
- [ ] All requirements installed (`pip install -r requirements.txt`)
- [ ] PyInstaller version 6.0+
- [ ] Build directory is clean
- [ ] No spaces in file paths
- [ ] Antivirus not blocking PyInstaller
- [ ] Running from project root directory
- [ ] All source files present (ethos_gui.py, tools/, config.py, etc.)

---

## Performance Optimization

### Startup Time
- Use `--onefile` for slower startup but single file
- Use `--onedir` for faster startup but multiple files

### File Size
- Enable UPX compression: `--upx-dir=/path/to/upx`
- Exclude unused modules in spec file
- Strip debug symbols: `strip=True` in spec

---

## Security Considerations

### Building Securely

1. **Never include secrets in the build:**
   - Don't include config.json with API keys
   - Don't hardcode credentials
   - Use environment variables

2. **Verify build integrity:**
   - Build in clean environment
   - Compare checksums
   - Test on multiple systems

3. **Code signing:**
   - Sign executables for distribution
   - Prevents tampering
   - Reduces false positives

---

## Support

### Build Issues
- Check PyInstaller documentation: https://pyinstaller.org
- Review error logs in build/warnings
- Test with `--console` flag for debug output

### Runtime Issues
- Check Windows Event Viewer for errors
- Run with console version for debug output
- Verify all dependencies are included

---

## Summary

**Quick Build:**
```bash
pip install -r requirements.txt
python build_executable.py
```

**Output:**
```
dist/EthosFinder.exe
```

**Test:**
```bash
cd dist
EthosFinder.exe
```

**Distribute:**
- Share the `EthosFinder.exe` file
- Include README.txt for users
- Consider code signing for production

---

## License & Legal

**Important:** This tool is for defensive security and educational purposes only. Ensure compliance with:
- Local laws regarding OSINT tools
- Terms of service for APIs used
- Privacy regulations (GDPR, CCPA, etc.)

Distribute responsibly and include appropriate disclaimers.

---

**Happy Building! 🚀**
