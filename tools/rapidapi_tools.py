import requests
from config import config, save_config

REQUEST_TIMEOUT = 10

def prompt_api_key(api_name, host):
    """Ask RapidAPI key and save it in config.json"""
    key = input(f"Enter RapidAPI key for {api_name}: ").strip()
    if not key:
        print("[!] No key provided!")
        return
    config["rapidapi_key"] = key
    config["rapidapi_hosts"][api_name] = host
    save_config()
    print(f"[+] API key for {api_name} saved.")

def query_rapidapi(api_name, endpoint, params=None):
    """Generic RAPID API request"""
    if api_name not in config["rapidapi_hosts"]:
        print(f"[!] API {api_name} not configured.")
        return {}
    if not config.get("rapidapi_key"):
        print("[!] No RapidAPI key set.")
        return {}
    
    host = config["rapidapi_hosts"][api_name]
    url = f"https://{host}/{endpoint.lstrip('/')}"
    headers = {
        "X-RapidAPI-Key": config["rapidapi_key"],
        "X-RapidAPI-Host": host
    }
    try:
        r = requests.get(url, headers=headers, params=params, timeout=REQUEST_TIMEOUT)
        return r.json() if r.status_code == 200 else {}
    except Exception as e:
        print(f"[!] RapidAPI request failed: {e}")
        return {}