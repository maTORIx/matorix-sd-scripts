import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
TRAINING_OPTION_PATH = os.path.join(BASE_DIR, "options.json")

def load_config():
    with open(CONFIG_PATH, "r") as f:
        data = json.load(f)
    os.chdir(BASE_DIR)
    
    data["sd_scripts_path"] = os.path.abspath(data["sd_scripts_path"])
    if not os.path.isdir(data["sd_scripts_path"]):
        raise ValueError("sd_scripts_path is not a valid directory, please check out the README.md")

    data["output_dir"] = os.path.abspath(data["output_dir"])
    if not os.path.isdir(data["output_dir"]):
        os.makedirs(data["output_dir"])
    return data

def load_training_options():
    with open(TRAINING_OPTION_PATH, "r") as f:
        data = json.load(f)
    return data

CONFIG = load_config()
TRAINING_OPTIONS = load_training_options()
