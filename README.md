# EthosFinder
# TRACE REVEAL CONNECT


OSINT Finder is a **console-based tool** designed for exploring public digital footprints in a responsible way.  
It provides a simple interactive menu and can check for public accounts or mentions based on:

- 📧 Email address  
- 📱 Phone number (with carrier & country detection)  
- 👤 Username / handle  

⚠️ **Important**: This tool uses only publicly available data (basic HTTP checks & web searches).  
It is intended for **research, education, and lawful use cases only**. Please respect privacy and legal frameworks.

---

## ✨ Features

- Interactive menu  
- 📧 Email lookup → quick web search for mentions  
- 📱 Phone number lookup → detect country & carrier (via [`phonenumbers`](https://pypi.org/project/phonenumbers/))  
- 👤 Handle lookup → check common platforms (Instagram, Twitter/X, GitHub, Reddit, TikTok, LinkedIn, YouTube, etc.)  
- 💾 Export results to JSON

## 🛣️ Upcoming features

Planned additions to the tool (future releases):

- 🔎 **Person search by full name** — allow searching using given name and family name to locate public profiles and mentions.  
- 📅 **Date of birth (when known)** — accept a birth date as an optional filter to narrow down matches.  
- 💼 **Occupation / job title (when known)** — use known occupation or company information to improve relevance of results.  
- 🗂️ **Multi-attribute matching** — combine name, date of birth, occupation and other public facts to better identify and filter digital footprints across sources.  
- ⚖️ **Privacy & compliance controls** — clearer consent checks, rate-limiting, and logging to ensure lawful usage.  

These features will focus on searching public sources and improving match quality while keeping privacy and legality in mind.

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
  3) Find accounts by PSEUDONYM / HANDLE 👤
  4) Exit

Enter the data when prompted.

View results directly in the console or save them to a JSON file.
