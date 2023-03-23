import os
import sys
import json
from config import *

GEN_IMG_PATH = os.path.join(SD_SCRIPTS_PATH, "gen_img_diffusers.py")

def load_prompts(path):
    with open(path, "r", encoding="utf-8") as f:
        metadata = json.load(f)
    prompts = []
    for filename in metadata:
        prompt = metadata[filename]["caption"] + "," + metadata[filename]["tags"]
        prompts.append(prompt)
    return prompts

def gen_img_diffusers(model_path, prompts, dst, images_per_prompt=1):
    # exec shell command
    abs_model_path = os.path.abspath(model_path)
    abs_dst = os.path.abspath(dst)
    abs_prompts_file_path = os.path.join(abs_dst, "tmp_prompts.txt")
    os.makedirs(abs_dst, exist_ok=True)
    os.chdir(SD_SCRIPTS_PATH)
    with open(abs_prompts_file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(prompts))
    os.system(f'''
    python {GEN_IMG_PATH} --ckpt {abs_model_path} --from_file {abs_prompts_file_path} --outdir {abs_dst} --images_per_prompt {images_per_prompt} --batch_size {TRAIN_BATCH_SIZE} --steps {GENERATION_STEPS} --sampler {GENERATION_SAMPLER}
    ''')
    os.remove(abs_prompts_file_path)

def main():
    model_path = os.path.abspath(sys.argv[1])
    metadata_path = os.path.abspath(sys.argv[2])
    dst = os.path.abspath(sys.argv[3])
    images_per_prompt = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    prompts = load_prompts(metadata_path)
    gen_img_diffusers(model_path, prompts, dst, images_per_prompt)

if __name__ == '__main__':
    main()