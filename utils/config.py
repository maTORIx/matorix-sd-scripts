import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")

def load_config():
    with open(CONFIG_PATH, "r") as f:
        data = json.load(f)
    path_check_keys = ["sd_scripts_path", "deepdanbooru_project_path"]
    for key in path_check_keys:
        os.chdir(BASE_DIR)
        data[key] = os.path.abspath(data[key])
        if not os.path.isdir(data[key]):
            raise ValueError(f"{key} is not a valid directory, please check out the README.md")
    data["output_dir"] = os.path.abspath(data["output_dir"])
    if not os.path.isdir(data["output_dir"]):
        os.makedirs(data["output_dir"])
    return data

CONFIG = load_config()