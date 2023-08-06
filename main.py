import os
import sys
import glob
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from utils.settings import CONFIG, BASE_DIR, TRAINING_OPTIONS
from utils import tagimg, generate_image, cache
import jinja2
import typing

root = tk.Tk()
root.title("matroix-sd-scripts")
root.option_add("*Font", "Consolas 11")
root.option_add("*Background", "white")
root.configure(background="white")

# style
style = ttk.Style()
style.configure("TButton", width=20, height=20, borderwidth=1, relief="flat", background="white", foreground="black", font="Consolas 11", anchor="center")
style.configure("TCombobox", width=20, borderwidth=1, relief="flat", background="white", foreground="black", font="Consolas 11", anchor="left")

CACHE = cache.load_cache()
default_args = CONFIG["training_default_args"]
row = -1
tk_values = {}

def next_row():
    global row
    row += 1
    return row

def add_checkbox(text: str):
    global row
    row += 1
    label = tk.Label(root, text=text)
    label.grid(row=row, column=0, sticky="w")
    var = tk.BooleanVar(value=CACHE.get(text, False))
    checkbox = tk.Checkbutton(root, variable=var)
    checkbox.grid(row=row, column=1, sticky="w")
    tk_values[text] = var
    return var

def add_option_menu(text: str, options: typing.List[str]):
    global row
    row += 1
    options = [str(x) for x in options]
    label = tk.Label(root, text=text)
    label.grid(row=row, column=0, sticky="w")
    var = tk.StringVar(value=CACHE.get(text, options[0]))
    combobox = ttk.Combobox(root, textvariable=var, values=options, style="TCombobox")
    combobox["values"] = options
    combobox.grid(row=row, column=1, sticky="w")
    # option_menu = ttk.OptionMenu(root, var, var.get(), *options, style="TOptionMenu")
    # option_menu.grid(row=row, column=1, sticky="w")
    tk_values[text] = var
    return var

def add_path_entry(text: str, dir=False):
    global row
    row += 1
    label = tk.Label(root, text=text)
    label.grid(row=row, column=0, sticky="w")
    var = tk.StringVar(value=CACHE.get(text, ""))
    entry = tk.Entry(root, textvariable=var)
    entry.grid(row=row, column=1, sticky="w")
    if dir:
        button = ttk.Button(root, text="Browse", command=lambda: var.set(filedialog.askdirectory()), style="TButton")
    else:
        button = ttk.Button(root, text="Browse", command=lambda: var.set(filedialog.askopenfilename()), style="TButton")
    button.grid(row=row, column=2)
    tk_values[text] = var
    return var

def add_entry(text: str, varType="string", initialValue=None):
    global row
    row += 1
    label = tk.Label(root, text=text)
    label.grid(row=row, column=0, sticky="w")
    if varType == "int":
        if initialValue is None:
            initialValue = 0
        var = tk.IntVar(value=CACHE.get(text, initialValue))
    elif varType == "double":
        if initialValue is None:
            initialValue = 0.0
        print(initialValue)
        var = tk.DoubleVar(value=CACHE.get(text, initialValue))
    elif varType == "string":
        if initialValue is None:
            initialValue = ""
        var = tk.StringVar(value=CACHE.get(text, initialValue))
    else:
        raise ValueError(f"Invalid varType: {varType}")
    entry = tk.Entry(root, textvariable=var)
    entry.grid(row=row, column=1, sticky="w")
    tk_values[text] = var
    return var

def add_label(text: str):
    global row
    row += 1
    label = tk.Label(root, text=text)
    label.grid(row=row, column=0, sticky="w")

def add_from_training_options(category, label):
    if category not in TRAINING_OPTIONS or label not in TRAINING_OPTIONS[category]:
        raise ValueError(f"Invalid category: {category} or label: {label}")
    option = TRAINING_OPTIONS[category][label]
    if category == "flags":
        add_checkbox(label)
    elif category == "values":
        add_entry(label, option["type"], option.get("default", None))
    elif category == "selects":
        add_option_menu(label, option["values"])
    elif category == "types":
        add_option_menu(label, option.keys())
    else:
        raise ValueError(f"Invalid category: {category}")

# model name
add_entry("Model Name")
add_checkbox("Is SDXL")
add_path_entry("Image Source Directory", dir=True)
add_path_entry("StableDiffusion Model Path")
add_path_entry("VAE Path")
add_label("Training options")
add_from_training_options("values", "steps")
add_entry("Batch Size", "int", 1)
add_from_training_options("flags", "Train U-Net only")
add_from_training_options("flags", "Enable image ratio bucket")
add_from_training_options("flags", "Cache latents")
add_from_training_options("types", "network")
add_from_training_options("types", "optimizer")
add_from_training_options("flags", "torch 2.0")
add_from_training_options("flags", "xformers")
add_from_training_options("values", "Caption dropout rate")
add_from_training_options("selects", "max token length")
add_from_training_options("flags", "shuffle caption")
add_entry("Identifier")
add_checkbox("Use Identifier Only")
add_entry("Class")
add_entry("Regularization images count", "int", -1)
add_from_training_options("selects", "sampler")
add_label("Augmentation")
add_from_training_options("flags", "Flip LR")
add_from_training_options("flags", "Color aug")
add_from_training_options("flags", "Random crop")

def get_values():
    values = {k: v.get() for k, v in tk_values.items()}
    values["dst"] = os.path.join(CONFIG["output_dir"], values["Model Name"])
    values["train_img_dst"] = os.path.join(values["dst"], "train")
    values["reg_img_dst"] = os.path.join(values["dst"], "reg")
    values["toml_path"] = os.path.join(values["dst"], "config.toml")
    values["sample_prompt_path"] = os.path.join(values["dst"], "prompt.txt")
    if values["Model Name"] == "":
        raise ValueError("Model Name cannot be empty")
    if values["Regularization images count"] == "":
        values["Regularization images count"] = 0 
    save_cache(values)

    if int(values["Regularization images count"]) < 0:
        values["Regularization images count"] = len(tagimg.find_images(values["Image Source Directory"]))
    return values

def save_cache(values):
    data = {}
    uncacheable_keys = ["dst", "train_img_dst", "reg_img_dst", "toml_path", "sample_prompt_path", "Model Name", "Image Source Directory"]
    for key in values.keys():
        if key not in uncacheable_keys:
            data[key] = values[key]
    cache.save_cache(data)

def run():
    values = get_values()

    # make dst directory
    if os.path.exists(values["dst"]):
        raise FileExistsError(f"{values['dst']} already exists")
    os.makedirs(values["dst"], exist_ok=False)

    # setup datasets
    tagimg.tagimg(values["Image Source Directory"], values["train_img_dst"], values["Identifier"])
    
    # generate images
    if values["Regularization images count"] > 0:
        os.makedirs(values["reg_img_dst"], exist_ok=True)
        if values["Class"] == "":
            prompts = generate_image.get_prompts_from_dir(
                values["train_img_dst"],
                values["Regularization images count"],
                CONFIG["generator"]["default_prompt"],
                CONFIG["generator"]["default_negative_prompt"]
            )
        else:
            prompt = generate_image.join_prompt(
                values["Class"],
                CONFIG["generator"]["default_prompt"],
                CONFIG["generator"]["default_negative_prompt"]
            )
            prompts = [prompt] * values["Regularization images count"]

        if (values["Is SDXL"]):
            generate_image.txt2img_sdxl(
                dst=values["reg_img_dst"],
                model_path=values["StableDiffusion Model Path"],
                vae_path=values["VAE Path"],
                sampler=values["sampler"],
                prompts=prompts
            )
        else:
            generate_image.txt2img(
                dst=values["reg_img_dst"],
                model_path=values["StableDiffusion Model Path"],
                vae_path=values["VAE Path"],
                sampler=values["sampler"],
                prompts=prompts
            )
    
    # generate config.toml
    with open(os.path.join(BASE_DIR, "templates", "config.toml.jinja2"), "r") as f:
        template = jinja2.Template(f.read())
    toml = template.render({"values": values, "CONFIG": CONFIG, "OPTIONS": TRAINING_OPTIONS})
    with open(values["toml_path"], "w", encoding="utf-8") as f:
        f.write(toml)

    # generate command.txt
    with open(os.path.join(BASE_DIR, "templates", "command.txt.jinja2"), "r") as f:
        template = jinja2.Template(f.read())
    command = template.render({"values": values, "CONFIG": CONFIG, "OPTIONS": TRAINING_OPTIONS})
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
    words = [values["Identifier"], values["Class"]]
    if not values["Use Identifier Only"]:
        caption_file_path = list(glob.glob(os.path.join(values["train_img_dst"], "*.txt")))[0]
        with open(caption_file_path, "r") as f:
            caption = f.read()
        words.append(caption)
    prompt = generate_image.join_prompt(
        ", ".join(filter(lambda x: x != "", words)),
        CONFIG["sample"]["default_prompt"],
        CONFIG["sample"]["default_negative_prompt"]
    )
    with open(os.path.join(values["sample_prompt_path"]), "w", encoding="utf-8") as f:
        f.write(prompt)
    
    # exit app
    print("matorix-sd-scripts task finished !")
    root.destroy()

# run button
next_row()
run_button = ttk.Button(root, text="Run", command=run, style="TButton")
run_button.grid(row=row, column=0, columnspan=3, sticky="e")

root.mainloop()