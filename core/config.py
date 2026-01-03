import json
import os

CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "last_folder": "",
    "fg_color": "#000000",
    "bg_color": "#ffffff",
    "box_size": 10,
    "open_folder": True
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return DEFAULT_CONFIG.copy()

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)
