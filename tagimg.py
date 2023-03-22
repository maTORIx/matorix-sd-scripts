import os
import sys
import shutil
from glob import glob

BLIP_BATCH_SIZE = 8
SD_SCRIPTS_PATH = "C:\\Users\\matorix\\src\\github.com\\kohya-ss\\sd-scripts"
DEEPDANBOORU_PROJECT_PATH = "C:\\Users\\matorix\\src\\github.com\\kohya-ss\\DeepDanbooru\\deepdanbooru-v3-20211112-sgd-e28"

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

def caption_blip(dir):
    # exec shell command
    os.system(f'python {BLIP_SCRIPT_PATH} --batch_size {BLIP_BATCH_SIZE} {dir}')

def caption_deepdanbooru(dir):
    # exec shell command
    os.system(f'deepdanbooru evaluate {dir} --project-path {DEEPDANBOORU_PROJECT_PATH} --allow-folder --save-txt')

def merge_captions(dir):
    # exec shell command
    json_path = os.path.join(dir, "meta_cap.json")
    os.system(f'python {CAPTION_SCRIPT_PATH} --full_path {dir} {json_path}')
    os.system(f'python {TAG_SCRIPT_PATH} --full_path {dir} {json_path}')

def clearning_captions(dir):
    # exec shell command
    load_json_path = os.path.join(dir, "meta_cap.json")
    save_json_path = os.path.join(dir, "meta_clean.json")
    os.system(f'python {CLEANING_SCRIPT_PATH} {load_json_path} {save_json_path}')

def main():
    os.chdir(SD_SCRIPTS_PATH)
    src = os.path.abspath(sys.argv[1])
    dst = os.path.abspath(sys.argv[2])
    copy_images(src, dst)
    caption_blip(dst)
    caption_deepdanbooru(dst)
    merge_captions(dst)
    clearning_captions(dst)

if __name__ == '__main__':
    main()
