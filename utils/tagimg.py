import os
import sys
import shutil
from glob import glob
import tqdm
from utils.settings import CONFIG
from utils import wd14tagger

SD_SCRIPTS_PATH = CONFIG["sd_scripts_path"]
BLIP_SCRIPT_PATH = os.path.join(SD_SCRIPTS_PATH, "finetune", "make_captions.py")
CAPTION_SCRIPT_PATH = os.path.join(SD_SCRIPTS_PATH, "finetune", "merge_captions_to_metadata.py")
TAG_SCRIPT_PATH = os.path.join(SD_SCRIPTS_PATH, "finetune", "merge_dd_tags_to_metadata.py")
CLEANING_SCRIPT_PATH = os.path.join(SD_SCRIPTS_PATH, "finetune", "clean_captions_and_tags.py")

def find_images(path):
    exts = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.webp']
    result = []
    for ext in exts:
        result.extend(glob(os.path.join(path, "**", ext), recursive=True))
    return [os.path.abspath(path) for path in result]

def copy_images(src, dst):
    images = find_images(src)
    os.makedirs(dst, exist_ok=True)
    for i, image in enumerate(images):
        filename = os.path.basename(image)
        shutil.copy(image, os.path.join(dst, f'{i:05d}_{filename}'))

def caption_blip(dir, identifier):
    # exec shell command
    os.system(f'python {BLIP_SCRIPT_PATH} --batch_size {CONFIG["tagger"]["blip_batch_size"]} "{dir}"')
    for path in glob(os.path.join(dir, "*.caption")):
        with open(path, "r") as f:
            caption = f.read()
        with open(path, "w") as f:
            if identifier and identifier != "":
                f.write(identifier + ", ")
            f.write(caption)

def caption_wd14(dir, identifier=""):
    print("Generating captions with WD14 model")
    images = find_images(dir)
    for image_path in tqdm.tqdm(images):
        tags = wd14tagger.generate_tags(image_path)
        caption_path = os.path.join(dir, os.path.splitext(os.path.basename(image_path))[0] + ".txt")
        with open(caption_path, "w") as f:
            if identifier and identifier != "":
                f.write(identifier + ", ")
            f.write(", ".join(tags))

def merge_captions(dir):
    # exec shell command
    json_path = os.path.join(dir, "meta_cap.json")
    os.system(f'python {CAPTION_SCRIPT_PATH} --full_path "{dir}" "{json_path}"')
    os.system(f'python {TAG_SCRIPT_PATH} --full_path "{dir}" "{json_path}"')

def clearning_captions(dir):
    # exec shell command
    load_json_path = os.path.join(dir, "meta_cap.json")
    save_json_path = os.path.join(dir, "meta_clean.json")
    os.system(f'python {CLEANING_SCRIPT_PATH} "{load_json_path}" "{save_json_path}"')

def tagimg(src, dst, identifier=""):
    os.chdir(SD_SCRIPTS_PATH)
    copy_images(src, dst)
    caption_blip(dst, identifier)
    caption_wd14(dst, identifier)
    merge_captions(dst)
    clearning_captions(dst)

def main():
    src = os.path.abspath(sys.argv[1])
    dst = os.path.abspath(sys.argv[2])
    tagimg(src, dst)
