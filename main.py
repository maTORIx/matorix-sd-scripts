import os
import glob
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from utils.settings import CONFIG, BASE_DIR, TRAINING_OPTIONS
from utils import tagimg, generate_image, cache
from utils.ui import setup_ui
import jinja2
import typing

ui = None


def get_params(values):
    params = values.copy()
    params["dst"] = os.path.join(CONFIG["output_dir"], params["Model Name"])
    params["train_img_dst"] = os.path.join(params["dst"], "train")
    params["reg_img_dst"] = os.path.join(params["dst"], "reg")
    params["toml_path"] = os.path.join(params["dst"], "config.toml")
    params["sample_prompt_path"] = os.path.join(params["dst"], "prompt.txt")
    if params["Model Name"] == "":
        raise ValueError("Model Name cannot be empty")
    if params["Regularization images count"] == "":
        params["Regularization images count"] = 0

    if int(params["Regularization images count"]) < 0:
        params["Regularization images count"] = len(
            tagimg.find_images(params["Image Source Directory"])
        )
    return params


def save_cache(values):
    tmp = values.copy()
    uncacheable = ["Image Source Directory", "Model Name", "Identifier", "Class"]
    for key in uncacheable:
        tmp.pop(key)
    cache.save_cache(tmp)

def run():
    values = ui.get_values()
    save_cache(values)
    params = get_params(values)

    # make dst directory
    if os.path.exists(params["dst"]):
        raise FileExistsError(f"{params['dst']} already exists")
    os.makedirs(params["dst"], exist_ok=False)

    # setup datasets
    tagimg.tagimg(
        params["Image Source Directory"], params["train_img_dst"], params["Identifier"]
    )

    # generate images
    if params["Regularization images count"] > 0:
        os.makedirs(params["reg_img_dst"], exist_ok=True)
        if params["Class"] == "":
            prompts = generate_image.get_prompts_from_dir(
                params["train_img_dst"],
                params["Regularization images count"],
                CONFIG["generator"]["default_prompt"],
                CONFIG["generator"]["default_negative_prompt"],
            )
        else:
            prompt = generate_image.join_prompt(
                params["Class"],
                CONFIG["generator"]["default_prompt"],
                CONFIG["generator"]["default_negative_prompt"],
            )
            prompts = [prompt] * params["Regularization images count"]

        if params["Is SDXL"]:
            generate_image.txt2img_sdxl(
                dst=params["reg_img_dst"],
                model_path=params["StableDiffusion Model Path"],
                vae_path=params["VAE Path"],
                sampler=params["sampler"],
                prompts=prompts,
            )
        else:
            generate_image.txt2img(
                dst=params["reg_img_dst"],
                model_path=params["StableDiffusion Model Path"],
                vae_path=params["VAE Path"],
                sampler=params["sampler"],
                prompts=prompts,
            )

    # generate config.toml
    with open(os.path.join(BASE_DIR, "templates", "config.toml.jinja2"), "r") as f:
        template = jinja2.Template(f.read())
    toml = template.render(
        {"values": params, "CONFIG": CONFIG, "OPTIONS": TRAINING_OPTIONS}
    )
    with open(params["toml_path"], "w", encoding="utf-8") as f:
        f.write(toml)

    # generate command.txt
    with open(os.path.join(BASE_DIR, "templates", "command.txt.jinja2"), "r") as f:
        template = jinja2.Template(f.read())
    command = template.render(
        {"values": params, "CONFIG": CONFIG, "OPTIONS": TRAINING_OPTIONS}
    )
    command = ("\n").join(
        filter(
            lambda line: len(line) > 0, [line.strip() for line in command.splitlines()]
        )
    )
    with open(os.path.join(params["dst"], "command.txt"), "w", encoding="utf-8") as f:
        f.write(command)

    # generate sctipts
    with open(os.path.join(BASE_DIR, "templates", "train.bat.jinja2"), "r") as f:
        template = jinja2.Template(f.read())
    script = template.render(
        {
            "values": params,
            "CONFIG": CONFIG,
            "command": " ^\n".join(command.splitlines()),
        }
    )
    with open(os.path.join(params["dst"], "train.bat"), "w", encoding="utf-8") as f:
        f.write(script)

    with open(os.path.join(BASE_DIR, "templates", "train.sh.jinja2"), "r") as f:
        template = jinja2.Template(f.read())
    script = template.render(
        {
            "values": params,
            "CONFIG": CONFIG,
            "command": " \\\n".join(command.splitlines()),
        }
    )
    with open(os.path.join(params["dst"], "train.sh"), "w", encoding="utf-8") as f:
        f.write(script)

    # generate prompt for generate sample
    words = [params["Identifier"], params["Class"]]
    if not params["Use Identifier Only"]:
        caption_file_path = list(
            glob.glob(os.path.join(params["train_img_dst"], "*.txt"))
        )[0]
        with open(caption_file_path, "r") as f:
            caption = f.read()
        words.append(caption)
    prompt = generate_image.join_prompt(
        ", ".join(filter(lambda x: x != "", words)),
        CONFIG["sample"]["default_prompt"],
        CONFIG["sample"]["default_negative_prompt"],
    )
    with open(os.path.join(params["sample_prompt_path"]), "w", encoding="utf-8") as f:
        f.write(prompt)

    # exit app
    print("matorix-sd-scripts task finished !")
    ui.destroy()


def main():
    global ui
    ui = setup_ui(cache.load_cache(), TRAINING_OPTIONS, run)
    ui.mainloop()


main()
