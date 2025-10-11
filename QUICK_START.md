# ETHOS FINDER v2 - Quick Start Guide

Get started with ETHOS FINDER in minutes!

---

## 🚀 For End Users (Using the Executable)

### Step 1: Get the Application
Download `EthosFinder.exe` from the releases

### Step 2: Run the Application
1. Double-click `EthosFinder.exe`
2. If Windows SmartScreen appears, click "More info" → "Run anyway"
   - This is normal for unsigned executables
3. The GUI will open automatically

### Step 3: Perform a Search

**Email Search:**
1. Click "📧 Email Search" tab
2. Enter an email address (e.g., example@domain.com)
3. Click "🔍 Search" or press Enter
4. View results in the panel below

**Phone Search:**
1. Click "📱 Phone Search" tab
2. Enter phone with country code (e.g., +1234567890)
3. Click "🔍 Search" or press Enter
4. See carrier info and WhatsApp link

**Username Search:**
1. Click "👤 Username Search" tab
2. Enter username (e.g., john_doe)
3. Click "🔍 Search" or press Enter
4. Check results across 25+ platforms

### Step 4: Export Results (Optional)
- Click **File → Export Results**
- Choose file type (.txt or .json)
- Save to your desired location

---

## 💻 For Developers (Running from Source)

### Step 1: Clone/Download Repository
```bash
git clone https://github.com/yourusername/EthosFinder.git
cd EthosFinder
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the GUI
```bash
python ethos_gui.py
```

**Or run the CLI version:**
```bash
python ethos.py
```

---

## 🔐 Configure API Keys (Optional)

For enhanced searches using RapidAPI:

### Method 1: Through GUI (Recommended)
1. Open ETHOS FINDER
2. Click **Settings → Configure API Keys**
3. Enter:
   - API Name: e.g., "Hunter.io"
   - API Host: e.g., "hunter-email-finder.p.rapidapi.com"
   - API Key: Your RapidAPI key
4. Click **Save**

### Method 2: Environment Variable (Most Secure)
```bash
# Windows
set ETHOS_RAPIDAPI_KEY=your_key_here

# Linux/Mac
export ETHOS_RAPIDAPI_KEY=your_key_here
```

### Method 3: Configuration File
Edit or create `config.json`:
```json
{
  "rapidapi_key": "your_key_here",
  "rapidapi_hosts": {
    "Hunter": "hunter-email-finder.p.rapidapi.com"
  }
}
```

**Note:** Keys are encrypted automatically when using secure_config.py

---

## 🛠️ Build Your Own Executable

### Quick Build
```bash
python build_executable.py
```

Follow the prompts:
1. Select build type (GUI-only, Console, or Both)
2. Wait for build to complete
3. Find executable in `dist/` folder

### Manual Build
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name=EthosFinder ethos_gui.py
```

See [BUILD_GUIDE.md](BUILD_GUIDE.md) for advanced options.

---

## 📋 Features Overview

### ✅ What You Can Do

**Email Search:**
- Find email mentions on the web
- Discover linked social profiles
- Validate email existence (with API)

**Phone Search:**
- Parse international phone numbers
- Identify carrier and country
- Generate WhatsApp links
- Lookup phone details (with API)

**Username Search:**
- Check 25+ platforms simultaneously
- Instagram, Twitter, GitHub, TikTok, Reddit, etc.
- Direct links to found profiles
- Status codes for verification

### ⚠️ What's Coming Soon
- Name/Surname search
- Public IP lookup
- WHOIS history
- Advanced export options

---

## 🎯 Usage Examples

### Example 1: Finding Social Profiles
```
1. Select "👤 Username Search"
2. Enter: "elonmusk"
3. Results show:
   ✓ Twitter: FOUND
   ✓ Instagram: FOUND
   ✓ GitHub: FOUND
   ... and 20+ more platforms
```

### Example 2: Phone Number Analysis
```
1. Select "📱 Phone Search"
2. Enter: "+14155552671"
3. Results show:
   - E.164: +14155552671
   - Country: United States
   - Carrier: Verizon
   - WhatsApp: https://wa.me/14155552671
```

### Example 3: Email Research
```
1. Select "📧 Email Search"
2. Enter: "contact@example.com"
3. Results show:
   - Web mentions (up to 20)
   - Possible social profiles
   - API data (if enabled)
```

---

## 🔒 Security & Privacy

### Best Practices
1. **Never share API keys** - They're like passwords
2. **Use environment variables** for production
3. **Don't commit config.json** to version control
4. **Review search results** before sharing
5. **Respect privacy** - Use for legitimate purposes only

### Data Storage
- Results are NOT saved automatically
- Config stored locally in `config.json`
- API keys encrypted with `cryptography`
- No telemetry or tracking

### Legal & Ethical Use
✅ **Allowed:**
- Background checks (with consent)
- Security research
- Personal investigations
- Educational purposes

❌ **NOT Allowed:**
- Harassment or stalking
- Unauthorized access
- Commercial use without license
- Violating terms of service

---

## 🆘 Troubleshooting

### Application Won't Start
**Solution:**
- Check if antivirus is blocking it
- Add exception for EthosFinder.exe
- Try console version for error messages

### "No Results Found"
**Solution:**
- Check internet connection
- Verify search query format
- Try different search type
- Enable API for enhanced results

### API Keys Not Working
**Solution:**
- Verify key in Settings → View Configuration
- Check API subscription status
- Ensure correct host URL
- Test with free tier API first

### Search Takes Too Long
**Solution:**
- Username search checks 25+ sites (30+ seconds normal)
- Phone/email searches are faster (5-10 seconds)
- Close other network-intensive apps
- Check firewall settings

### Export Not Working
**Solution:**
- Ensure write permissions in target folder
- Choose different save location
- Check disk space
- Try different file format

---

## 📞 Support & Community

### Documentation
- [SECURITY_IMPROVEMENTS.md](SECURITY_IMPROVEMENTS.md) - Security features
- [BUILD_GUIDE.md](BUILD_GUIDE.md) - Building from source
- Built-in Help: **Help → Documentation**

### Getting Help
1. Check this Quick Start guide
2. Review built-in documentation
3. Search existing issues on GitHub
4. Open new issue with details

### Contributing
Contributions welcome! Please:
- Fork the repository
- Create feature branch
- Submit pull request
- Follow code style

---

## ⚡ Tips & Tricks

### Power User Features
1. **Keyboard Shortcuts:**
   - Press `Enter` after typing to search
   - `Ctrl+A` to select all results
   - `Ctrl+C` to copy results

2. **Batch Searches:**
   - Search multiple targets
   - Export each result
   - Combine in spreadsheet

3. **API Integration:**
   - Enable checkbox for enhanced results
   - Prompts only when API configured
   - Falls back to free search if declined

4. **Result Analysis:**
   - Copy JSON results to analyze
   - Use tools like jq or Python for parsing
   - Export for reporting

### Performance Tips
- **Fast searches:** Disable API for quick results
- **Comprehensive:** Enable API for detailed data
- **Parallel:** Run multiple instances for batch work
- **Export:** Save results immediately for reference

---

## 📊 Comparison: CLI vs GUI

| Feature | CLI (ethos.py) | GUI (ethos_gui.py) |
|---------|----------------|-------------------|
| User Interface | Text menu | Graphical tabs |
| Search Types | All supported | All supported |
| API Integration | Yes (interactive) | Yes (checkbox) |
| Export Results | Manual copy | File → Export |
| Settings | Menu-based | Graphical dialog |
| Best For | Scripts, automation | Interactive use |
| Compilation | Not needed | Can be .exe |

**Recommendation:**
- Use **GUI** for regular searches
- Use **CLI** for scripting/automation

---

## 🎓 Learning Resources

### OSINT Basics
- Understanding OSINT: https://osintframework.com
- Legal considerations
- Ethical guidelines

### Python & Tools
- Python basics: https://python.org/doc
- Requests library
- Tkinter GUI programming

### Security
- Cryptography basics
- API key management
- Secure coding practices

---

## ✨ What's Next?

After getting started:
1. ✅ Perform your first search
2. ✅ Configure API keys (optional)
3. ✅ Try all search types
4. ✅ Export and analyze results
5. ✅ Explore advanced features

**Happy Investigating! 🔍**

---

**Version:** 2.0
**Last Updated:** 2025
**License:** See LICENSE file
**Disclaimer:** For educational and defensive security purposes only
