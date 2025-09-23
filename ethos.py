import sys
import json
import requests
import re
import time
from typing import Dict, List
try:
    import phonenumbers
    from phonenumbers import geocoder, carrier, NumberParseException
except Exception:
    phonenumbers = None

# --- CONFIG ---
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/72.0.3582.0 Safari/537.36"
REQUEST_TIMEOUT = 6 # seconds
RATE_LIMIT_DELAY = 0.5 # seconds between requests

SOCIAL_PLATFORMS = {
    "Instagram": "https://www.instagram.com/{handle}/",
    "Twitter": "https://twitter.com/{handle}",
    "X": "https://x.com/{handle}",
    "Facebook": "https://www.facebook.com/{handle}",
    "GitHub": "https://github.com/{handle}",
    "Reddit": "https://www.reddit.com/user/{handle}",
    "TikTok": "https://www.tiktok.com/@{handle}",
    "LinkedIn": "https://www.linkedin.com/in/{handle}",
    "Pinterest": "https://www.pinterest.com/{handle}/",
    "YouTube": "https://www.youtube.com/{handle}",
}

# common email-profile patterns (some sites allow search by email in URL, rare)
EMAIL_PATTERNS = [
    # later you could plug APIs that accept email search
]

# --- ASCII ART ---
ASCII_ART = r"""

                  ,----,                                                                                                              
                ,/   .`|       ,--,    ,----..                                                 ,--.                                   
    ,---,.    ,`   .'  :     ,--.'|   /   /   \   .--.--.               ,---,.   ,---,       ,--.'|    ,---,        ,---,.,-.----.    
  ,'  .' |  ;    ;     /  ,--,  | :  /   .     : /  /    '.           ,'  .' |,`--.' |   ,--,:  : |  .'  .' `\    ,'  .' |\    /  \   
,---.'   |.'___,/    ,',---.'|  : ' .   /   ;.  \  :  /`. /         ,---.'   ||   :  :,`--.'`|  ' :,---.'     \ ,---.'   |;   :    \  
|   |   .'|    :     | |   | : _' |.   ;   /  ` ;  |  |--`          |   |   .':   |  '|   :  :  | ||   |  .`\  ||   |   .'|   | .\ :  
:   :  |-,;    |.';  ; :   : |.'  |;   |  ; \ ; |  :  ;_            :   :  :  |   :  |:   |   \ | ::   : |  '  |:   :  |-,.   : |: |  
:   |  ;/|`----'  |  | |   ' '  ; :|   :  | ; | '\  \    `.         :   |  |-,'   '  ;|   : '  '; ||   ' '  ;  ::   |  ;/||   |  \ :  
|   :   .'    '   :  ; '   |  .'. |.   |  ' ' ' : `----.   \        |   :  ;/||   |  |'   ' ;.    ;'   | ;  .  ||   :   .'|   : .  /  
|   |  |-,    |   |  ' |   | :  | ''   ;  \; /  | __ \  \  |        |   |   .''   :  ;|   | | \   ||   | :  |  '|   |  |-,;   | |  \  
'   :  ;/|    '   :  | '   : |  : ; \   \  ',  / /  /`--'  /        '   :  '  |   |  ''   : |  ; .''   : | /  ; '   :  ;/||   | ;\  \ 
|   |    \    ;   |.'  |   | '  ,/   ;   :    / '--'.     /         |   |  |  '   :  ||   | '`--'  |   | '` ,/  |   |    \:   ' | \.' 
|   :   .'    '---'    ;   : ;--'     \   \ .'    `--'---'          |   :  \  ;   |.' '   : |      ;   :  .'    |   :   .':   : :-'   
|   | ,'               |   ,/          `---`                        |   | ,'  '---'   ;   |.'      |   ,.'      |   | ,'  |   |.'     
`----'                 '---'                                        `----'            '---'        '---'        `----'    `---'       
                                                                                                                                      
    ETHOS FINDER    -   v1.0
"""

# --- Helpers ---
def http_head(url: str) -> Dict:
    """Try HEAD then GET fallback. Return dict with status_code and final _url."""
    headers = {"User-Agent": USER_AGENT}
    try:
        resp = requests.head(url, headers=headers, allow_redirects=True, timeout=REQUEST_TIMEOUT)
        # some sites reject HEAD -> fallback to GET
        if resp.status_code >=400:
            resp = requests.get(url, headers=headers, allow_redirects=True, timeout=REQUEST_TIMEOUT)
        return {"status_code": resp.status_code, "url": resp.url, "ok": resp.ok}
    except requests.RequestException as e:
        return {"status_code": None, "url": url, "ok": False, "error": str(e)}
    
def polite_request_delay():
    time.sleep(RATE_LIMIT_DELAY)

def save_json(filename: str, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[+] Results saved to {filename}")

# ------- OSINT functions -------
def find_by_handle(handle: str) -> Dict:
    """
    Check a list of common social platforms for the presence of `handle`.
    Returns a dict of platform -> {exists:bool, status_code, url}
    """
    print(f"[i] Checking handle: {handle}")
    results = {}
    for name, pattern in SOCIAL_PLATFORMS.items():
        url = pattern.format(handle=handle)
        res = http_head(url)
        exists = res.get("ok", False) and res.get("status_code", 0) < 400
        results[name] = {"exists": exists, "status_code": res.get("status_code"), "url": res.get("url")}
        print(f" - {name:<9}: {'FOUND' if exists else 'not found'} (status={res.get('status_code')})")
        polite_request_delay()
    return results

def find_by_email(email: str) -> Dict:
    """
    Basic email OSINT:
    - Validate simple email format
    - Do a web search (DuckDuckGo HTML quick search) for the email (public mentions)
    - Try pattern checks for social platforms where emails appear publicly (rare)
    NOTE: For production, prefer APIs (Hunter, FullContact, etc.) with proper keys.
    """
    print(f"[i] Searching for public mentions of email: {email}")
    results = {"email": email, "mentions": []}

    # simple email validation
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        print("[!] That doesn't look like a valid email address.")
        return results

    # Quick web search using DuckDuckGo HTML interface (lightweight)
    # We fetch results page and extract links (best-effort)
    query = requests.utils.requote_uri(email)
    ddg_url = f"https://html.duckduckgo.com/html?q={query}"
    try:
        headers = {"User-Agent": USER_AGENT}
        r = requests.post(ddg_url, headers=headers, timeout=REQUEST_TIMEOUT)
        if r.status_code == 200:
            # naive link extraction
            links = re.findall(r'href="(https?://[^"]+)"', r.text)
            # filter and unique
            uniq = []
            for link in links:
                if email in link or len(uniq) < 10:
                    if link not in uniq:
                        uniq.append(link)
            results["mentions"] = uniq[:20]
            print(f"[+] Found ~{len(results['mentions'])} potential mentions (sample).")
        else:
            print(f"[!] DuckDuckGo search returned status {r.status_code}")
    except Exception as e:
        print(f"[!] Web search failed: {e}")

    # Optionally check common profile pages that sometimes display emails (rare):
    # (placeholder - no direct URL patterns for email -> profiles)
    polite_request_delay()
    return results

def find_by_phone(raw_phone: str) -> Dict:
    """
    Parse phone number with phonenumbers (if available) and try to detect country and carrier.
    Then optionally check common social platforms for phone number exposure (not implemented).
    """
    print(f"[i] Analyzing phone number: {raw_phone}")
    data = {"input": raw_phone, "parsed": None, "country": None, "carrier": None, "possible_profiles": {}}

    if phonenumbers is None:
        print("[!] phonenumbers library not installed. Install with: pip install phonenumbers")
        return data

    try:
        # Try to parse with no region first, fallback to 'US'
        try:
            num = phonenumbers.parse(raw_phone, None)
        except NumberParseException:
            # try with default region (you can change)
            num = phonenumbers.parse(raw_phone, "US")

        data["parsed"] = phonenumbers.format_number(num, phonenumbers.PhoneNumberFormat.E164)
        data["country"] = geocoder.description_for_number(num, "en")
        data["carrier"] = carrier.name_for_number(num, "en")
        print(f" - E.164: {data['parsed']}")
        print(f" - Country: {data['country']}")
        print(f" - Carrier: {data['carrier'] or 'unknown'}")
    except NumberParseException as e:
        print(f"[!] Could not parse number: {e}")
        return data

    # Basic idea: some social platforms expose phone-based recovery endpoints or allow to search by phone via APIs.
    # For now, we'll check a few services that support phone-based profiles via URL patterns (best-effort):
    # WARNING: Many platforms do not expose profiles by phone in URLs; real detection requires APIs.
    # We'll check WhatsApp link format and signal-like patterns (public presence only).
    possible = {}
    # WhatsApp via wa.me/ - not a public profile per se, but a clickable number link:
    possible["WhatsApp_clicktochat"] = {"url": f"https://wa.me/{data['parsed'].lstrip('+')}", "note": "click-to-chat (does not confirm account existence)"}
    # Telegram user by phone is not discoverable by URL unless user has @username
    polite_request_delay()
    data["possible_profiles"] = possible
    return data

# ------- UI / Menu -------
def print_header():
    print(ASCII_ART)
    print("Ethics note: Use this tool only for lawful & permitted research.\n")

def menu():
    print_header()
    print("Choose an option:")
    print("  1) Find accounts by EMAIL (unstable)")
    print("  2) Find accounts by PHONE NUMBER (and detect operator/country)")
    print("  3) Find accounts by PSEUDONYM / HANDLE")
    print("  4) Exit")
    choice = input("\nEnter choice (1-4): ").strip()
    return choice

def run():
    while True:
        choice = menu()
        if choice == "1":
            email = input("Enter email address: ").strip()
            res = find_by_email(email)
            print(json.dumps(res, indent=2, ensure_ascii=False))
            if input("Save results? (y/N): ").strip().lower() == "y":
                filename = f"email_{re.sub('[^0-9a-zA-Z@._-]','_',email)}.json"
                save_json(filename, res)
            input("\nPress Enter to return to menu...")
        elif choice == "2":
            phone = input("Enter phone number (with +country): ").strip()
            res = find_by_phone(phone)
            print(json.dumps(res, indent=2, ensure_ascii=False))
            if input("Save results? (y/N): ").strip().lower() == "y":
                safe_phone = re.sub('[^0-9+]','_', phone)
                filename = f"phone_{safe_phone}.json"
                save_json(filename, res)
            input("\nPress Enter to return to menu...")
        elif choice == "3":
            handle = input("Enter pseudonym / handle (without @): ").strip().lstrip("@")
            res = find_by_handle(handle)
            print(json.dumps(res, indent=2, ensure_ascii=False))
            if input("Save results? (y/N): ").strip().lower() == "y":
                filename = f"handle_{re.sub('[^0-9a-zA-Z_-]','_',handle)}.json"
                save_json(filename, res)
            input("\nPress Enter to return to menu...")
        elif choice == "4":
            print("Give us a star on GitHub!")
            sys.exit(0)
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print("\nInterrupted — exiting.")
        sys.exit(0)