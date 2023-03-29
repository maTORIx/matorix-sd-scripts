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
default_args = CONFIG["training_default_args"]

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
sd_path_var = tk.StringVar(value=CACHE.get("sd_path", ""))
sd_path_entry = tk.Entry(root, textvariable=sd_path_var)
sd_path_entry.grid(row=2, column=1)
sd_path_button = tk.Button(root, text="Browse", command=lambda: sd_path_entry.insert(0, filedialog.askopenfilename()))
sd_path_button.grid(row=2, column=2)

# training options
train_label = tk.Label(root, text="Training Options")
train_label.grid(row=3, column=0, sticky="w")

steps_label = tk.Label(root, text="Steps")
steps_label.grid(row=4, column=0, sticky="w")
steps_var = tk.IntVar(value=CACHE.get("steps", default_args["steps"]))
steps_entry = tk.Entry(root, textvariable=steps_var)
steps_entry.grid(row=4, column=1)

batch_label = tk.Label(root, text="Batch Size")
batch_label.grid(row=5, column=0, sticky="w")
batch_size_var = tk.IntVar(value=CACHE.get("batch_size", default_args["batch_size"]))
batch_entry = tk.Entry(root, textvariable=batch_size_var)
batch_entry.grid(row=5, column=1)

learning_rate_label = tk.Label(root, text="Learning Rate")
learning_rate_label.grid(row=6, column=0, sticky="w")
learning_rate_var = tk.DoubleVar(value=CACHE.get("learning_rate", default_args["learning_rate"]))
learning_rate_entry = tk.Entry(root, textvariable=learning_rate_var)
learning_rate_entry.grid(row=6, column=1)

enable_bucket_label = tk.Label(root, text="Enable image ratio bucket")
enable_bucket_label.grid(row=7, column=0, sticky="w")
enable_bucket_var = tk.BooleanVar(value=True)
enable_bucket_checkbox = tk.Checkbutton(root, variable=enable_bucket_var)
enable_bucket_checkbox.grid(row=7, column=1)

xformers_label = tk.Label(root, text="Xformers")
xformers_label.grid(row=8, column=0, sticky="w")
xformers_var = tk.BooleanVar(value=CACHE.get("xformers", default_args["xformers"]))
xformers_checkbox = tk.Checkbutton(root, variable=xformers_var)
xformers_checkbox.grid(row=8, column=1)

# network
network_label = tk.Label(root, text="Network")
network_label.grid(row=9, column=0, sticky="w")
network_var = tk.StringVar(value=CACHE.get("network", default_args["network"]))
network_choices = CONFIG["training_types"]["networks"].keys()
network_option = tk.OptionMenu(root, network_var, *network_choices)
network_option.grid(row=9, column=1)

# optimizer
optimizer_label = tk.Label(root, text="Optimizer")
optimizer_label.grid(row=10, column=0, sticky="w")
optimizer_var = tk.StringVar(value=CACHE.get("optimizer", default_args["optimizer"]))
optimizer_choices = CONFIG["training_types"]["optimizers"].keys()
optimizer_option = tk.OptionMenu(root, optimizer_var, *optimizer_choices)
optimizer_option.grid(row=10, column=1)

# identifier
identifier_label = tk.Label(root, text="Identifier")
identifier_label.grid(row=11, column=0, sticky="w")
identifier_var = tk.StringVar(value="")
identifier_entry = tk.Entry(root, textvariable=identifier_var)
identifier_entry.grid(row=11, column=1)

# class
class_label = tk.Label(root, text="Class")
class_label.grid(row=12, column=0, sticky="w")
class_var = tk.StringVar(value="")
class_entry = tk.Entry(root, textvariable=class_var)
class_entry.grid(row=12, column=1)

# regularization images count
reg_count_label = tk.Label(root, text="Regularization images count")
reg_count_label.grid(row=13, column=0, sticky="w")
reg_count_var = tk.IntVar(value=0)
reg_count_entry = tk.Entry(root, textvariable=reg_count_var)
reg_count_entry.grid(row=13, column=1)

# augmentation
augmentation_label = tk.Label(root, text="Augmentation")
augmentation_label.grid(row=14, column=0, sticky="w")

fliplr_label = tk.Label(root, text="fliplr")
fliplr_label.grid(row=15, column=0, sticky="w")
fliplr_var = tk.BooleanVar(value=default_args["fliplr"])
fliplr_checkbox = tk.Checkbutton(root, variable=fliplr_var)
fliplr_checkbox.grid(row=15, column=1)

coloraug_label = tk.Label(root, text="color_aug")
coloraug_label.grid(row=16, column=0, sticky="w")
coloraug_var = tk.BooleanVar(value=default_args["color_aug"])
coloraug_checkbox = tk.Checkbutton(root, variable=coloraug_var)
coloraug_checkbox.grid(row=16, column=1)

randomcrop_label = tk.Label(root, text="random_crop")
randomcrop_label.grid(row=17, column=0, sticky="w")
randomcrop_var = tk.BooleanVar(value=default_args["random_crop"])
randomcrop_checkbox = tk.Checkbutton(root, variable=randomcrop_var)
randomcrop_checkbox.grid(row=17, column=1)

catptiondropoutrate_label = tk.Label(root, text="caption_dropout_rate")
catptiondropoutrate_label.grid(row=18, column=0, sticky="w")
catptiondropoutrate_var = tk.DoubleVar(value=default_args["caption_dropout_rate"])
catptiondropoutrate_entry = tk.Entry(root, textvariable=catptiondropoutrate_var)
catptiondropoutrate_entry.grid(row=18, column=1)



def get_values():
    values = {
        "model_name": model_output_name_entry.get(),
        "src": src_entry.get(),
        "sd_path": sd_path_entry.get(),
        "steps": steps_var.get(),
        "batch_size": batch_size_var.get(),
        "learning_rate": learning_rate_var.get(),
        "enable_bucket": enable_bucket_var.get(),
        "xformers": xformers_var.get(),
        "network": network_var.get(),
        "optimizer": optimizer_var.get(),
        "identifier": identifier_var.get(),
        "class": class_var.get(),
        "reg_count": reg_count_var.get(),
        "fliplr": fliplr_var.get(),
        "color_aug": coloraug_var.get(),
        "random_crop": randomcrop_var.get(),
        "caption_dropout_rate": catptiondropoutrate_var.get(),
    }
    values["dst"] = os.path.join(CONFIG["output_dir"], values["model_name"])
    values["train_img_dst"] = os.path.join(values["dst"], "train")
    values["reg_img_dst"] = os.path.join(values["dst"], "reg")
    values["toml_path"] = os.path.join(values["dst"], "config.toml")
    values["sample_prompt_path"] = os.path.join(values["dst"], "prompt.txt")

    if values["reg_count"] < 0:
        values["reg_count"] = len(tagimg.find_images(values["src"]))
    return values

def save_cache(values):
    old = cache.load_cache()
    cacheable = [
        "sd_path",
        "network",
        "optimizer",
        "xformers",
        "steps",
        "batch_size",
        "learning_rate",
    ]
    for key in cacheable:
        if old.get(key, None) != values[key]:
            old[key] = values[key]
    cache.save_cache(old)

def run():
    values = get_values()
    save_cache(values)
    if os.path.exists(values["dst"]):
        raise FileExistsError(f"{values['dst']} already exists")
    # setup directories
    os.makedirs(values["dst"], exist_ok=False)
    # setup datasets
    # tagimg.tagimg(values["src"], values["train_img_dst"])
    # if values["reg_count"] > 0:
    #     os.makedirs(values["reg_img_dst"], exist_ok=True)
    #     if values["class"] == "":
    #         generate_image.transparent_img(values["reg_img_dst"], values["reg_count"])
    #     else:
    #         generate_image.txt2img(
    #             model_path=values["sd_path"],
    #             prompt=f"""{values['class']}, {CONFIG["generator"]["default_prompt"]}""",
    #             negative_prompt=CONFIG["generator"]["default_negative_prompt"],
    #             dst=values["reg_img_dst"],
    #             count=values["reg_count"],
    #         )
    
    # generate config.toml
    with open(os.path.join(BASE_DIR, "templates", "config.toml.jinja2"), "r") as f:
        template = jinja2.Template(f.read())
    toml = template.render({"values": values, "CONFIG": CONFIG})
    with open(values["toml_path"], "w", encoding="utf-8") as f:
        f.write(toml)

    # generate command.txt
    with open(os.path.join(BASE_DIR, "templates", "command.txt.jinja2"), "r") as f:
        template = jinja2.Template(f.read())
    command = template.render({"values": values, "CONFIG": CONFIG})
    command = ("\n").join(filter(lambda line: len(line) > 0, [line.strip() for line in command.splitlines()]))
    with open(os.path.join(values["dst"], "command.txt"), "w", encoding="utf-8") as f:
        f.write(command)
    
    # generate sctipts
    with open(os.path.join(BASE_DIR, "templates", "train.bat.jinja2"), "r") as f:
        template = jinja2.Template(f.read())
    script = template.render({"values": values, "CONFIG": CONFIG, "command": " ^\n".join(command.splitlines())})
    with open(os.path.join(values["dst"], "train.bat"), "w", encoding="utf-8") as f:
        f.write(script)

    with open(os.path.join(BASE_DIR, "templates", "train.sh.jinja2"), "r") as f:
        template = jinja2.Template(f.read())
    script = template.render({"values": values, "CONFIG": CONFIG, "command": " \\\n".join(command.splitlines())})
    with open(os.path.join(values["dst"], "train.sh"), "w", encoding="utf-8") as f:
        f.write(script)
    
    # generate prompt for generate sample
    # if values["identifier"] != "":
    #     prompt = f"""{CONFIG["sample"]["default_prompt"]}, {values["identifier"]} {values["class"]} --n {CONFIG["sample"]["default_negative_prompt"]}"""
    # else:
    #     caption_file_path = list(glob.glob(os.path.join(values["train_img_dst"], "*.caption")))[0]
    #     with open(caption_file_path, "r") as f:
    #         caption = f.read()
    #     prompt = f"""{CONFIG["sample"]["default_prompt"]}, {caption} --n {CONFIG["sample"]["default_negative_prompt"]}"""
    # prompts = filter(lambda x: x != "", prompt.replace("\n", "").split(","))
    # prompt = (", ").join([s.strip() for s in prompts])
    # with open(os.path.join(values["sample_prompt_path"]), "w", encoding="utf-8") as f:
    #     f.write(prompt)
    
    # exit app
    print("matorix-sd-scripts task finished !")
    root.destroy()

# run button
run_button = tk.Button(root, text="Run", command=run)
run_button.grid(row=19, column=0, columnspan=3)

root.mainloop()