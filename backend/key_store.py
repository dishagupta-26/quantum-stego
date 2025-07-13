# key_store.py
import json
import os

KEY_FILE = "key_registry.json"

def save_key(key_id, key):
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "r") as f:
            data = json.load(f)
    else:
        data = {}

    data[key_id] = key
    with open(KEY_FILE, "w") as f:
        json.dump(data, f)

def load_key(key_id):
    if not os.path.exists(KEY_FILE):
        raise ValueError("No key registry found")

    with open(KEY_FILE, "r") as f:
        data = json.load(f)

    if key_id not in data:
        raise ValueError(f"No key found for ID: {key_id}")

    return data[key_id]
