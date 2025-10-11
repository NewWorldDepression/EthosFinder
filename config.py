# config.py

import json
import os

CONFIG_FILE = "config.json"

# Default values
config = {
    "rapidapi_key": "",
    "rapidapi_hosts": {}
}

def load_config():
    """Load configuration from file. Returns config dict or creates default if not exists."""
    global config
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                loaded_config = json.load(f)
                # Validate config structure
                if not isinstance(loaded_config, dict):
                    raise ValueError("Config file must contain a JSON object")
                config.update(loaded_config)
                print(f"[+] Configuration loaded from {CONFIG_FILE}")
        except json.JSONDecodeError as e:
            print(f"[!] Error parsing config file: {e}")
            print("[i] Using default configuration. Consider resetting config.")
        except Exception as e:
            print(f"[!] Error reading config file: {e}")
            print("[i] Using default configuration.")
    else:
        print(f"[i] No config file found. Using defaults.")
    return config

def save_config():
    """Save configuration to file with error handling."""
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
        print(f"[+] Configuration saved to {CONFIG_FILE}")
        return True
    except Exception as e:
        print(f"[!] Error saving config: {e}")
        return False