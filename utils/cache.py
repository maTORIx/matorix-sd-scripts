import os
import json
from utils.config import BASE_DIR

CACHE_PATH = os.path.join(BASE_DIR, ".cache.json")

def save_cache(cache):
    with open(CACHE_PATH, "w") as f:
        f.write(json.dumps(cache))

def load_cache():
    if not os.path.exists(CACHE_PATH):
        return {}
    with open(CACHE_PATH, "r") as f:
        return json.loads(f.read())
