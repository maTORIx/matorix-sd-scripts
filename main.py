import os
import sys
import glob
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from utils.config import CONFIG, BASE_DIR
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

# model name
add_entry("Model Name")
add_checkbox("Is SDXL")
add_path_entry("Image Source Directory", dir=True)
add_path_entry("StableDiffusion Model Path")
add_path_entry("VAE Path")
add_label("Training Options")
add_entry("Steps", "int", 6000)
add_entry("Batch Size", "int", 4)
add_entry("Learning Rate", "double", 1e-4)
add_checkbox("Train U-Net Only")
add_checkbox("Enable image ratio bucket")
add_checkbox("Cache latents")
add_checkbox("xformers")
add_option_menu("Network", CONFIG["training_types"]["networks"].keys())
add_option_menu("Optimizer", CONFIG["training_types"]["optimizers"].keys())
add_entry("Caption Dropout Rate", "double")
add_checkbox("Suffle Caption")
add_option_menu("Network", CONFIG["training_types"]["networks"].keys())
add_entry("Identifier")
add_entry("Class")
add_entry("Regularization images count", "int", -1)
add_label("Augmentation")
add_checkbox("Flip LR")
add_checkbox("Color Aug")
add_checkbox("Random Crop")
add_label("Sample output")
add_option_menu("sampler", CONFIG["sample"]["samplers"])

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
        values["Regularization images count"] = -1
    

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
    save_cache(values)

    # make dst directory
    if os.path.exists(values["dst"]):
        raise FileExistsError(f"{values['dst']} already exists")
    os.makedirs(values["dst"], exist_ok=False)

    # setup datasets
    tagimg.tagimg(values["Image Source Directory"], values["train_img_dst"])
    if values["Regularization images count"] > 0:
        os.makedirs(values["reg_img_dst"], exist_ok=True)
        if values["Class"] == "":
            if (values["Is SDXL"]):
                generate_image.transparent_img(values["reg_img_dst"], values["Regularization images count"], 1024, 1024)
            else:
                generate_image.transparent_img(values["reg_img_dst"], values["Regularization images count"])
        else:
            if (values["Is SDXL"]):
                generate_image.txt2img_sdxl(
                    model_path=values["StableDiffusion Model Path"],
                    vae_path=values["VAE Path"],
                    sampler=values["sampler"],
                    prompt=f"""{values['Class']}, {CONFIG["generator"]["default_prompt"]}""",
                    negative_prompt=CONFIG["generator"]["default_negative_prompt"],
                    dst=values["reg_img_dst"],
                    count=values["Regularization images count"],
                )
            else:
                generate_image.txt2img(
                    model_path=values["StableDiffusion Model Path"],
                    vae_path=values["VAE Path"],
                    sampler=values["sampler"],
                    prompt=f"""{values['Class']}, {CONFIG["generator"]["default_prompt"]}""",
                    negative_prompt=CONFIG["generator"]["default_negative_prompt"],
                    dst=values["reg_img_dst"],
                    count=values["Regularization images count"],
                )
    
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
    if values["Identifier"] != "":
        prompt = f"""{values["Identifier"]}, {values["Class"]}, {CONFIG["sample"]["default_prompt"]} --n {CONFIG["sample"]["default_negative_prompt"]}"""
    else:
        caption_file_path = list(glob.glob(os.path.join(values["train_img_dst"], "*.txt")))[0]
        with open(caption_file_path, "r") as f:
            caption = f.read()
        prompt = f"""{CONFIG["sample"]["default_prompt"]}, {caption} --n {CONFIG["sample"]["default_negative_prompt"]}"""
    prompts = filter(lambda x: x != "", prompt.replace("\n", "").split(","))
    prompt = (", ").join([s.strip() for s in prompts])
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