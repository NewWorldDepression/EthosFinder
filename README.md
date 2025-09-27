# EthosFinder
# TRACE REVEAL CONNECT

EthosFinder is a modular OSINT tool designed to help researchers, cybersecurity enthusiasts, and investigators gather publicly available information about emails, phone numbers, social media handles, and more. **Use responsibly and only for lawful purposes.**

---

## Features

### 1. Modular Search Tools
- **Email Search** (`email_search.py`)
  - Basic web search (Google, DuckDuckGo, Bing, Yandex)
  - Detect potential social profiles associated with emails
  - Optionally enrich results using RapidAPI services
  - Save search results interactively

- **Phone Number Search** (`phone_search.py`)
  - Parses phone numbers with `phonenumbers`
  - Detects E.164 format, country, and carrier
  - Suggests possible public profiles (e.g., WhatsApp click-to-chat)
  - Optionally query RapidAPI for enhanced data
  - Save search results interactively

- **Handle / Pseudonym Search** (`handle_search.py`)
  - Checks common social media platforms (Instagram, Twitter, TikTok, GitHub, LinkedIn, YouTube, Discord, Reddit, etc.)
  - Optionally query RapidAPI for enhanced results
  - Save search results interactively

### 2. Settings
- Configure RapidAPI key(s) and API hosts via **settings menu**
- Reset all settings with a single click

### 3. Future Features
Planned for future versions:
- Search by full name (first + last) to detect social profiles
- Search by public IP to detect location and ISP
- WHOIS lookup for domain information
- Additional OSINT modules for social media, public records, and more

---


## 📦 Requirements

- Python **3.8+**  
- [Requests](https://pypi.org/project/requests/)  
- [phonenumbers](https://pypi.org/project/phonenumbers/) (optional, for 📱 phone lookups)

Install dependencies:

```bash
pip install -r requirements.txt
````

## 🚀 Usage

1. Clone or download this repository.  
2. Run the script:

```bash
python ethos.py
```
**Choose an option from the menu**:
  1) Find accounts by EMAIL 📧
  2) Find accounts by PHONE NUMBER 📱
  3) Find accounts by USERNAME 👤
  4) Exit

Enter the data when prompted.

View results directly in the console.
