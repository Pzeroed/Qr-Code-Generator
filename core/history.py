import json
import os

HISTORY_FILE = "history.json"
MAX_HISTORY = 20

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                return json.load(f).get("entries", [])
        except:
            pass
    return []

def save_history(entries):
    entries = entries[-MAX_HISTORY:]
    with open(HISTORY_FILE, "w") as f:
        json.dump({"entries": entries}, f, indent=4)
    return entries
