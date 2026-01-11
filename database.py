import json
import os

DB_FILE = "data.json"

def load_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({"groups": {}}, f)
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_group(group_id):
    data = load_db()
    gid = str(group_id)
    if gid not in data["groups"]:
        data["groups"][gid] = {
            "force_join": False,
            "force_channel": None
        }
        save_db(data)
    return data["groups"][gid]

def set_force_channel(group_id, channel):
    data = load_db()
    gid = str(group_id)
    if gid not in data["groups"]:
        get_group(group_id)
        data = load_db()
    data["groups"][gid]["force_channel"] = channel
    save_db(data)

def set_force_join(group_id, value: bool):
    data = load_db()
    gid = str(group_id)
    if gid not in data["groups"]:
        get_group(group_id)
        data = load_db()
    data["groups"][gid]["force_join"] = value
    save_db(data)
