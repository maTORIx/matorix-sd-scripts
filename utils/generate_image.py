import os
from PIL import Image
from utils.config import CONFIG

GEN_IMG_PATH = os.path.join(CONFIG["sd_scripts_path"], "gen_img_diffusers.py")
GEN_IMG_SDXL_PATH = os.path.join(CONFIG["sd_scripts_path"], "sdxl_gen_img.py")

def transparent_img(dir, n, h=512, w=512):
    # generate n transparent images
    for i in range(n):
        path = os.path.join(dir, f"{i}.png")
        img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        img.save(path)

def txt2img(model_path, vae_path, sampler, prompt, negative_prompt, dst, count=1):
    # exec shell command
    abs_model_path = os.path.abspath(model_path)
    abs_dst = os.path.abspath(dst)
    os.makedirs(abs_dst, exist_ok=True)
    os.chdir(CONFIG["sd_scripts_path"])
    command = f'''python "{GEN_IMG_PATH}"
        --ckpt "{abs_model_path}"
        --outdir "{abs_dst}"
        --vae "{os.path.abspath(vae_path)}"
        --no_half_vae
        --images_per_prompt {count}
        --batch_size {CONFIG["generator"]["batch_size"]}
        --steps {CONFIG["generator"]["steps"]}
        --sampler {sampler}
        --prompt "{prompt} {f"--n {negative_prompt}" if negative_prompt else ""}"
    '''
    print((" ").join([x.strip() for x in command.splitlines()]))
    os.system((" ").join([x.strip() for x in command.splitlines()]))

def txt2img_sdxl(model_path, vae_path, sampler, prompt, negative_prompt, dst, count=1):
    # exec shell command
    abs_model_path = os.path.abspath(model_path)
    abs_dst = os.path.abspath(dst)
    os.makedirs(abs_dst, exist_ok=True)
    os.chdir(CONFIG["sd_scripts_path"])
    command = f'''python "{GEN_IMG_SDXL_PATH}"
        --ckpt "{abs_model_path}"
        --no_half_vae
        --vae "{os.path.abspath(vae_path)}"
        --outdir "{abs_dst}"
        --images_per_prompt {count}
        --batch_size {CONFIG["generator"]["batch_size"]}
        --steps {CONFIG["generator"]["steps"]}
        --sampler {sampler}
        --prompt "{prompt} {f"--n {negative_prompt}" if negative_prompt else ""}"
        --H 1024
        --W 1024
    '''
    print((" ").join([x.strip() for x in command.splitlines()]))
    os.system((" ").join([x.strip() for x in command.splitlines()]))