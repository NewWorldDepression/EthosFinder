# tools/email_search.py

import re
import requests
from time import sleep
from typing import Dict, List
from config import config, save_config
from tools import rapidapi_tools

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
REQUEST_TIMEOUT = 10

# ---------------------------
# Helpers
# ---------------------------
def polite_request_delay(seconds: int = 1):
    sleep(seconds)

def validate_email(email: str) -> bool:
    """Simple regex validation for email addresses."""
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

# ---------------------------
# Web Search (without API)
# ---------------------------
def search_web(email: str, engines: List[str] = None) -> List[str]: # type: ignore
    """Search email mentions on the web using HTML search engines (no API)."""
    if engines is None:
        engines = ["duckduckgo"]

    mentions = []

    for engine in engines:
        try:
            query = requests.utils.requote_uri(email)
            headers = {"User-Agent": USER_AGENT}

            if engine.lower() == "duckduckgo":
                url = f"https://html.duckduckgo.com/html?q={query}"
                r = requests.post(url, headers=headers, timeout=REQUEST_TIMEOUT)
            elif engine.lower() == "google":
                url = f"https://www.google.com/search?q={query}"
                r = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
            elif engine.lower() == "bing":
                url = f"https://www.bing.com/search?q={query}"
                r = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
            elif engine.lower() == "yandex":
                url = f"https://yandex.com/search/?text={query}"
                r = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
            else:
                continue

            if r.status_code == 200:
                links = re.findall(r'href="(https?://[^"]+)"', r.text)
                for link in links:
                    if email in link or len(mentions) < 10:
                        if link not in mentions:
                            mentions.append(link)
            polite_request_delay()
        except Exception as e:
            print(f"[!] {engine} search failed: {e}")

    return mentions[:20]

# ---------------------------
# Social Profiles
# ---------------------------
def search_social_profiles(email: str) -> Dict[str, str]:
    """Try to find social profiles linked to an email (basic patterns)."""
    patterns = {
        "GitHub": f"https://github.com/search?q={email}",
        "LinkedIn": f"https://www.linkedin.com/search/results/people/?keywords={email}",
        "Twitter": f"https://twitter.com/search?q={email}",
        "Facebook": f"https://www.facebook.com/search/top?q={email}"
    }
    return patterns

# ---------------------------
# Main Email Search
# ---------------------------
def find_by_email(email: str) -> Dict:
    """
    Search for an email in two steps:
    1) Public web search (no API)
    2) Optionally use RapidAPI for enhanced search
    """
    results = {"email": email, "mentions": [], "social_profiles": {}, "api_info": {}}

    if not validate_email(email):
        print("[!] That doesn't look like a valid email address.")
        return results

    # --- Step 1: Web search (without API) ---
    print(f"[i] Searching public mentions for email: {email} (no API)...")
    results["mentions"] = search_web(email)
    results["social_profiles"] = search_social_profiles(email)

    print(f"[+] Found {len(results['mentions'])} mentions on web search.")
    print("Social profile patterns checked (not verified existence).")

    # --- Step 2: Ask user if they want to continue with RapidAPI ---
    if config.get("rapidapi_key") and config.get("rapidapi_hosts"):
        choice = input("Do you want to continue the search using RapidAPI for enhanced results? (y/N): ").strip().lower()
        if choice == "y":
            # Iterate over all configured APIs that could handle email
            for api_name, host in config["rapidapi_hosts"].items():
                print(f"[i] Querying {api_name} via RapidAPI...")
                endpoint = f"verifier?email={email}"  # assuming Hunter-like endpoint
                api_result = rapidapi_tools.query_rapidapi(api_name, endpoint)
                if api_result:
                    results["api_info"][api_name] = api_result
    else:
        print("[!] No RapidAPI key configured. You can set it in the settings menu.")

    return results

# ---------------------------
# Batch search
# ---------------------------
def find_emails_info(emails: List[str]) -> List[Dict]:
    return [find_by_email(email) for email in emails]

# ---------------------------
# Example usage
# ---------------------------
if __name__ == "__main__":
    email = input("Enter an email address to search: ").strip()
    result = find_by_email(email)
    import json
    print(json.dumps(result, indent=2, ensure_ascii=False))

