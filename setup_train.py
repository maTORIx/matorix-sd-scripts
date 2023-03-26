import os
import sys
import glob
import tkinter as tk
from tkinter import filedialog
from utils.config import CONFIG, BASE_DIR
from utils import tagimg, generate_image, cache
import jinja2


root = tk.Tk()
CACHE = cache.load_cache()

# model name
model_output_name_label = tk.Label(root, text="Model Name")
model_output_name_label.grid(row=0, column=0, sticky="w")
model_output_name_var = tk.StringVar(value="")
model_output_name_entry = tk.Entry(root, textvariable=model_output_name_var)
model_output_name_entry.grid(row=0, column=1)

# src directory
src_label = tk.Label(root, text="Source Directory")
src_label.grid(row=1, column=0, sticky="w")
src_entry = tk.Entry(root)
src_entry.grid(row=1, column=1)
src_button = tk.Button(root, text="Browse", command=lambda: src_entry.insert(0, filedialog.askdirectory()))
src_button.grid(row=1, column=2)

# stable diffusion directory
sd_path_label = tk.Label(root, text="StableDiffusion model path")
sd_path_label.grid(row=2, column=0, sticky="w")
sd_path_var = tk.StringVar(value="" if CACHE.get("sd_path") is None else CACHE.get("sd_path"))
sd_path_entry = tk.Entry(root, textvariable=sd_path_var)
sd_path_entry.grid(row=2, column=1)
sd_path_button = tk.Button(root, text="Browse", command=lambda: sd_path_entry.insert(0, filedialog.askopenfilename()))
sd_path_button.grid(row=2, column=2)

# training options
train_label = tk.Label(root, text="Training Options")
train_label.grid(row=3, column=0, sticky="w")

steps_label = tk.Label(root, text="Steps")
steps_label.grid(row=4, column=0, sticky="w")
steps_var = tk.IntVar(value=25000)
steps_entry = tk.Entry(root, textvariable=steps_var)
steps_entry.grid(row=4, column=1)

batch_label = tk.Label(root, text="Batch Size")
batch_label.grid(row=5, column=0, sticky="w")
batch_var = tk.IntVar(value=4)
batch_entry = tk.Entry(root, textvariable=batch_var)
batch_entry.grid(row=5, column=1)

learning_rate_label = tk.Label(root, text="Learning Rate")
learning_rate_label.grid(row=6, column=0, sticky="w")
learning_rate_var = tk.DoubleVar(value=1e-4)
learning_rate_entry = tk.Entry(root, textvariable=learning_rate_var)
learning_rate_entry.grid(row=6, column=1)

enable_bucket_label = tk.Label(root, text="Enable image ratio bucket")
enable_bucket_label.grid(row=7, column=0, sticky="w")
enable_bucket_var = tk.BooleanVar(value=True)
enable_bucket_checkbox = tk.Checkbutton(root, variable=enable_bucket_var)
enable_bucket_checkbox.grid(row=7, column=1)

# identifier
identifier_label = tk.Label(root, text="Identifier")
identifier_label.grid(row=8, column=0, sticky="w")
identifier_var = tk.StringVar(value="")
identifier_entry = tk.Entry(root, textvariable=identifier_var)
identifier_entry.grid(row=8, column=1)

# class
class_label = tk.Label(root, text="Class")
class_label.grid(row=9, column=0, sticky="w")
class_var = tk.StringVar(value="")
class_entry = tk.Entry(root, textvariable=class_var)
class_entry.grid(row=9, column=1)

# regularization images count
reg_count_label = tk.Label(root, text="Regularization images count")
reg_count_label.grid(row=10, column=0, sticky="w")
reg_count_var = tk.IntVar(value=0)
reg_count_entry = tk.Entry(root, textvariable=reg_count_var)
reg_count_entry.grid(row=10, column=1)

# run options
run_options_label = tk.Label(root, text="Run Options")
run_options_label.grid(row=11, column=0, sticky="w")



def get_values():
    values = {
        "model_name": model_output_name_entry.get(),
        "src": os.path.abspath(src_entry.get()),
        "sd_path": os.path.abspath(sd_path_entry.get()),
        "steps": steps_var.get(),
        "batch_size": batch_var.get(),
        "learning_rate": learning_rate_var.get(),
        "enable_bucket": enable_bucket_var.get(),
        "identifier": identifier_var.get(),
        "class": class_var.get(),
        "reg_count": reg_count_var.get(),
    }
    values["images_dst"] = os.path.join(CONFIG["output_dir"], values["model_name"])
    values["model_dst"] = os.path.join(CONFIG["output_dir"], values["model_name"])
    values["train_img_dst"] = os.path.join(values["images_dst"], "train")
    values["reg_img_dst"] = os.path.join(values["images_dst"], "reg")
    values["toml_path"] = os.path.join(values["images_dst"], "config.toml")
    values["sample_prompt_path"] = os.path.join(values["images_dst"], "prompt.txt")

    if values["reg_count"] < 0:
        values["reg_count"] = len(tagimg.find_images(values["src"]))
    return values

def save_cache(values):
    old = cache.load_cache()
    if old.get("sd_path", None) != values["sd_path"]:
        old["sd_path"] = values["sd_path"]
        cache.save_cache(old)

def run():
    values = get_values()
    save_cache(values)

    # setup datasets
    tagimg.tagimg(values["src"], values["train_img_dst"])
    if values["reg_count"] > 0:
        os.makedirs(values["reg_img_dst"], exist_ok=True)
        if values["class"] == "":
            generate_image.transparent_img(values["reg_img_dst"], values["reg_count"])
        else:
            generate_image.txt2img(
                model_path=values["sd_path"],
                prompt=f"""{values['class']}, {CONFIG["generator"]["default_prompt"]}""",
                negative_prompt=CONFIG["generator"]["default_negative_prompt"],
                dst=values["reg_img_dst"],
                count=values["reg_count"],
            )
    
    # generate config.toml
    with open(os.path.join(BASE_DIR, "templates", "config.toml.jinja2"), "r") as f:
        template = jinja2.Template(f.read())
    toml = template.render({"values": values, "CONFIG": CONFIG})
    with open(values["toml_path"], "w", encoding="utf-8") as f:
        f.write(toml)

    # generate train.sh
    with open(os.path.join(BASE_DIR, "templates", "train.sh.jinja2"), "r") as f:
        template = jinja2.Template(f.read())
    sh = template.render({"values": values, "CONFIG": CONFIG, "PYTHON_PATH": sys.base_prefix})
    sh = (" ").join([line.strip() for line in sh.splitlines()])
    with open(os.path.join(values["images_dst"], "train.sh"), "w", encoding="utf-8") as f:
        f.write(sh)
    
    # generate prompt for generate sample
    if values["identifier"] != "":
        prompt = f"""{CONFIG["sample"]["default_prompt"]}, {values["identifier"]} {values["class"]} --n {CONFIG["sample"]["default_negative_prompt"]}"""
    else:
        caption_file_path = list(glob.glob(os.path.join(values["train_img_dst"], "*.caption")))[0]
        with open(caption_file_path, "r") as f:
            caption = f.read()
        prompt = f"""{CONFIG["sample"]["default_prompt"]}, {caption} --n {CONFIG["sample"]["default_negative_prompt"]}"""
    prompts = filter(lambda x: x != "", prompt.replace("\n", "").split(","))
    prompt = (", ").join([s.strip() for s in prompts])
    with open(os.path.join(values["sample_prompt_path"]), "w", encoding="utf-8") as f:
        f.write(prompt)
    
    print("matorix-sd-scripts task finished !")
    
    # exit app
    root.destroy()

# run button
run_button = tk.Button(root, text="Run", command=run)
run_button.grid(row=12, column=0, columnspan=3)

root.mainloop()