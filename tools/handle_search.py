# tools/handle_search.py

import time
from typing import Dict
from config import config
from tools import rapidapi_tools
import requests

RATE_LIMIT_DELAY = 0.5

# ---------------------------
# Extended social platforms
# ---------------------------
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
    "Snapchat": "https://www.snapchat.com/add/{handle}",
    "Twitch": "https://www.twitch.tv/{handle}",
    "Discord": "https://discord.com/users/{handle}",  # profile URLs can vary
    "Medium": "https://medium.com/@{handle}",
    "Dribbble": "https://dribbble.com/{handle}",
    "Behance": "https://www.behance.net/{handle}",
    "Flickr": "https://www.flickr.com/people/{handle}/",
    "SoundCloud": "https://soundcloud.com/{handle}",
    "Steam": "https://steamcommunity.com/id/{handle}",
    "Spotify": "https://open.spotify.com/user/{handle}",
    "GitLab": "https://gitlab.com/{handle}",
    "Vimeo": "https://vimeo.com/{handle}",
    "Patreon": "https://www.patreon.com/{handle}",
    "StackOverflow": "https://stackoverflow.com/users/{handle}",
    "Goodreads": "https://www.goodreads.com/{handle}",
    "Letterboxd": "https://letterboxd.com/{handle}/",
    "ProductHunt": "https://www.producthunt.com/@{handle}",
}

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"

# ---------------------------
# Helpers
# ---------------------------
def polite_request_delay(seconds: float = RATE_LIMIT_DELAY):
    time.sleep(seconds)

def http_head(url: str) -> Dict:
    """Try HEAD then GET fallback. Return dict with status_code and final url."""
    headers = {"User-Agent": USER_AGENT}
    try:
        resp = requests.head(url, headers=headers, allow_redirects=True, timeout=5)
        if resp.status_code >= 400:
            resp = requests.get(url, headers=headers, allow_redirects=True, timeout=5)
        return {"status_code": resp.status_code, "url": resp.url, "ok": resp.ok}
    except requests.RequestException as e:
        return {"status_code": None, "url": url, "ok": False, "error": str(e)}

# ---------------------------
# Main handle search
# ---------------------------
def find_by_handle(handle: str) -> Dict:
    """
    Search for a handle across common social platforms.
    Step 1: check platforms locally
    Step 2: optionally continue with RapidAPI for enhanced search
    """
    handle = handle.lstrip("@")
    results = {"handle": handle, "platforms": {}, "api_info": {}}

    print(f"[i] Checking handle: {handle} on common platforms (no API)...")
    for name, pattern in SOCIAL_PLATFORMS.items():
        url = pattern.format(handle=handle)
        res = http_head(url)
        exists = res.get("ok", False) and res.get("status_code", 0) < 400
        results["platforms"][name] = {"exists": exists, "status_code": res.get("status_code"), "url": res.get("url")}
        print(f" - {name:<12}: {'FOUND' if exists else 'not found'} (status={res.get('status_code')})")
        polite_request_delay()

    # --- Ask user if they want to continue with RapidAPI ---
    if config.get("rapidapi_key") and config.get("rapidapi_hosts"):
        choice = input("Do you want to continue the search using RapidAPI for enhanced results? (y/N): ").strip().lower()
        if choice == "y":
            for api_name, host in config["rapidapi_hosts"].items():
                print(f"[i] Querying {api_name} via RapidAPI...")
                # Example endpoint (to be adapted per API)
                endpoint = f"handle-search?username={handle}"
                api_result = rapidapi_tools.query_rapidapi(api_name, endpoint)
                if api_result:
                    results["api_info"][api_name] = api_result
    else:
        print("[!] No RapidAPI key configured. You can set it in the settings menu.")

    return results

# ---------------------------
# Example usage
# ---------------------------
if __name__ == "__main__":
    handle = input("Enter pseudonym / handle (without @): ").strip()
    res = find_by_handle(handle)
    import json
    print(json.dumps(res, indent=2, ensure_ascii=False))
