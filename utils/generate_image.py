import os
from PIL import Image
from utils.config import CONFIG

GEN_IMG_PATH = os.path.join(CONFIG["sd_scripts_path"], "gen_img_diffusers.py")

def transparent_img(dir, n, h=512, w=512):
    # generate n transparent images
    for i in range(n):
        path = os.path.join(dir, f"{i}.png")
        img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        img.save(path)

def txt2img(model_path, prompt, negative_prompt, dst, count=1):
    # exec shell command
    abs_model_path = os.path.abspath(model_path)
    abs_dst = os.path.abspath(dst)
    os.makedirs(abs_dst, exist_ok=True)
    os.chdir(CONFIG["sd_scripts_path"])
    command = f'''python "{GEN_IMG_PATH}"
        --ckpt "{abs_model_path}"
        --outdir "{abs_dst}"
        --images_per_prompt {count}
        --batch_size {CONFIG["generator"]["batch_size"]}
        --steps {CONFIG["generator"]["steps"]}
        --sampler {CONFIG["generator"]["sampler"]}
        --prompt "{prompt} {f"--n {negative_prompt}" if negative_prompt else ""}"
    '''
    os.system((" ").join([x.strip() for x in command.splitlines()]))
