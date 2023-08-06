import os
from PIL import Image
from utils.settings import CONFIG
import glob

GEN_IMG_PATH = os.path.join(CONFIG["sd_scripts_path"], "gen_img_diffusers.py")
GEN_IMG_SDXL_PATH = os.path.join(CONFIG["sd_scripts_path"], "sdxl_gen_img.py")

def join_prompt(prompt, default_prompt, default_negative_prompt):
    result = prompt.strip()
    if default_prompt != "":
        if not default_prompt.endswith(","):
            result = default_prompt + "," + result
        else:
            result = default_prompt + result
    result = ", ".join(filter(lambda x: x != "", [x.strip() for x in result.split(",")]))
    if default_negative_prompt != "":
        prompt = prompt + " --n " + default_negative_prompt
    return prompt

def get_prompts_from_dir(dir, n=-1, default_prompt="", default_negative_prompt=""):
    files = glob.glob(os.path.join(dir, "*.txt"))
    if n == -1:
        n = len(files)
    prompts = []
    for i in range(n):
        with open(files[i % len(files)], "r") as f:
            prompt = join_prompt(f.read().strip(), default_prompt, default_negative_prompt)
            prompts.append(prompt)
    return prompts

def transparent_img(dir, n, h=512, w=512):
    # generate n transparent images
    for i in range(n):
        path = os.path.join(dir, f"{i}.png")
        img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        img.save(path)

def txt2img(dst, model_path, vae_path, sampler, prompts):
    # exec shell command
    abs_model_path = os.path.abspath(model_path)
    abs_dst = os.path.abspath(dst)
    os.makedirs(abs_dst, exist_ok=True)
    os.chdir(CONFIG["sd_scripts_path"])
    with open(os.path.join(abs_dst, "prompts.txt"), "w") as f:
        f.write("\n".join(prompts))
    command = f'''python "{GEN_IMG_PATH}"
        --ckpt "{abs_model_path}"
        --outdir "{abs_dst}"
        --vae "{os.path.abspath(vae_path)}"
        --images_per_prompt 1
        --batch_size {CONFIG["generator"]["batch_size"]}
        --steps {CONFIG["generator"]["steps"]}
        --sampler {sampler}
        --from_file "{os.path.join(abs_dst, "prompts.txt")}"
    '''
    print((" ").join([x.strip() for x in command.splitlines()]))
    os.system((" ").join([x.strip() for x in command.splitlines()]))

    for i, path in enumerate(sorted(glob.glob(os.path.join(abs_dst, "*.png")))):
        with open(os.path.splitext(path)[0] + ".txt", "w") as f:
            f.write(prompts[i])

def txt2img_sdxl(dst, model_path, vae_path, sampler, prompts):
    # exec shell command
    abs_model_path = os.path.abspath(model_path)
    abs_dst = os.path.abspath(dst)
    os.makedirs(abs_dst, exist_ok=True)
    os.chdir(CONFIG["sd_scripts_path"])
    with open(os.path.join(abs_dst, "prompts.txt"), "w") as f:
        f.write("\n".join(prompts))
    command = f'''python "{GEN_IMG_SDXL_PATH}"
        --ckpt "{abs_model_path}"
        --no_half_vae
        --vae "{os.path.abspath(vae_path)}"
        --outdir "{abs_dst}"
        --images_per_prompt 1
        --batch_size {CONFIG["generator"]["batch_size"]}
        --steps {CONFIG["generator"]["steps"]}
        --sampler {sampler}
        --from_file "{os.path.join(abs_dst, "prompts.txt")}"
        --H 1024
        --W 1024
    '''
    print((" ").join([x.strip() for x in command.splitlines()]))
    os.system((" ").join([x.strip() for x in command.splitlines()]))

    for i, path in enumerate(sorted(glob.glob(os.path.join(abs_dst, "*.png")))):
        with open(os.path.splitext(path)[0] + ".txt", "w") as f:
            f.write(prompts[i])