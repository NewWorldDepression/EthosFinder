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
    global config
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)
        return config
    
def save_config():
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)