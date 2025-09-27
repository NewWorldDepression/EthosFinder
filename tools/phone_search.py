# tools/phone_search.py

import re
import time
from typing import Dict
try:
    import phonenumbers
    from phonenumbers import geocoder, carrier, NumberParseException
except ImportError:
    phonenumbers = None

from config import config
from tools import rapidapi_tools

RATE_LIMIT_DELAY = 0.5  # seconds

# ---------------------------
# Helpers
# ---------------------------
def polite_request_delay(seconds: float = RATE_LIMIT_DELAY):
    time.sleep(seconds)

def parse_phone_number(raw_phone: str) -> Dict:
    """Parse a phone number and return basic info (E.164, country, carrier)."""
    data = {"input": raw_phone, "parsed": None, "country": None, "carrier": None, "possible_profiles": {}}

    if phonenumbers is None:
        print("[!] phonenumbers library not installed. Install with: pip install phonenumbers")
        return data

    try:
        try:
            num = phonenumbers.parse(raw_phone, None)
        except NumberParseException:
            num = phonenumbers.parse(raw_phone, "US")  # fallback region

        data["parsed"] = phonenumbers.format_number(num, phonenumbers.PhoneNumberFormat.E164)
        data["country"] = geocoder.description_for_number(num, "en")
        data["carrier"] = carrier.name_for_number(num, "en") or "unknown"

        print(f" - E.164: {data['parsed']}")
        print(f" - Country: {data['country']}")
        print(f" - Carrier: {data['carrier']}")

    except NumberParseException as e:
        print(f"[!] Could not parse number: {e}")
        return data

    return data

# ---------------------------
# Main Phone Search
# ---------------------------
def find_by_phone(raw_phone: str) -> Dict:
    """
    Search a phone number in two steps:
    1) Parse and basic analysis using phonenumbers (no API)
    2) Optionally continue with RapidAPI for enhanced search
    """
    results = parse_phone_number(raw_phone)

    # Add some basic "profiles" idea (example: WhatsApp click-to-chat)
    if results.get("parsed"):
        results["possible_profiles"] = {
            "WhatsApp_clicktochat": {
                "url": f"https://wa.me/{results['parsed'].lstrip('+')}",
                "note": "Click-to-chat (does not confirm account existence)"
            }
        }

    # --- Ask user if they want to continue with RapidAPI ---
    if config.get("rapidapi_key") and config.get("rapidapi_hosts"):
        choice = input("Do you want to continue the search using RapidAPI for enhanced results? (y/N): ").strip().lower()
        if choice == "y":
            # Iterate over all configured APIs that could handle phone numbers
            for api_name, host in config["rapidapi_hosts"].items():
                print(f"[i] Querying {api_name} via RapidAPI...")
                # Example endpoint (to be adapted per API)
                endpoint = f"phone-lookup?number={results.get('parsed')}"
                api_result = rapidapi_tools.query_rapidapi(api_name, endpoint)
                if api_result:
                    results.setdefault("api_info", {})[api_name] = api_result
    else:
        print("[!] No RapidAPI key configured. You can set it in the settings menu.")

    return results

# ---------------------------
# Example usage
# ---------------------------
if __name__ == "__main__":
    raw_phone = input("Enter phone number (with +country code): ").strip()
    res = find_by_phone(raw_phone)
    import json
    print(json.dumps(res, indent=2, ensure_ascii=False))
