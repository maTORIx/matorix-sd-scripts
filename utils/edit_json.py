import os
import sys
import json

def edit_dict(data, key, value):
    keys = key.split(".")
    for k in keys[:-1]:
        data = data[k]
    data[keys[-1]] = value
    return data

def edit_json(json_path, key, value):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    data = edit_dict(key, value, data)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    json_path = os.path.join(os.getcwd(), sys.argv[1])
    key = sys.argv[2]
    value = sys.argv[3]
    edit_json(json_path, key, value)
    print(f"Edit {key} to {value} in {json_path} successfully!")
