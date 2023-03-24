import os
import sys
import tkinter as tk
from tkinter import filedialog
from glob import glob
import gen_transparent
import genregression
import tagimg

root = tk.Tk()

# src directory
src_label = tk.Label(root, text="Source Directory")
src_label.grid(row=0, column=0, sticky="w")
src_entry = tk.Entry(root)
src_entry.grid(row=0, column=1)
src_button = tk.Button(root, text="Browse", command=lambda: src_entry.insert(0, filedialog.askdirectory()))
src_button.grid(row=0, column=2)

# dst directory
dst_label = tk.Label(root, text="Output Directory")
dst_label.grid(row=1, column=0, sticky="w")
dst_entry = tk.Entry(root)
dst_entry.grid(row=1, column=1)
dst_button = tk.Button(root, text="Browse", command=lambda: dst_entry.insert(0, filedialog.askdirectory()))
dst_button.grid(row=1, column=2)

# training options
train_label = tk.Label(root, text="Training Options")
train_label.grid(row=2, column=0, sticky="w")

steps_label = tk.Label(root, text="Steps")
steps_label.grid(row=3, column=0, sticky="w")
steps_var = tk.IntVar(value=25000)
steps_entry = tk.Entry(root, textvariable=steps_var)
steps_entry.grid(row=3, column=1)

batch_label = tk.Label(root, text="Batch Size")
batch_label.grid(row=4, column=0, sticky="w")
batch_var = tk.IntVar(value=4)
batch_entry = tk.Entry(root, textvariable=batch_var)
batch_entry.grid(row=4, column=1)

learning_rate_label = tk.Label(root, text="Learning Rate")
learning_rate_label.grid(row=5, column=0, sticky="w")
learning_rate_var = tk.DoubleVar(value=1e-4)
learning_rate_entry = tk.Entry(root, textvariable=learning_rate_var)
learning_rate_entry.grid(row=5, column=1)

enable_bucket_label = tk.Label(root, text="Enable image ratio bucket")
enable_bucket_label.grid(row=6, column=0, sticky="w")
enable_bucket_var = tk.BooleanVar(value=True)
enable_bucket_checkbox = tk.Checkbutton(root, variable=enable_bucket_var)
enable_bucket_checkbox.grid(row=6, column=1)

# training type
train_type_label = tk.Label(root, text="Training Type")
train_type_label.grid(row=7, column=0, sticky="w")
training_type_list = ["class+identifier", "caption+class(dreambooth)", "finetune"]
training_type_var = tk.StringVar(value=training_type_list[1])
training_type_menu = tk.OptionMenu(root, training_type_var, *training_type_list)
training_type_menu.grid(row=7, column=1)

description = """
When use class+identifier. Fill identifier and class.
When use caption+class(dreambooth). Fill class.
When use finetune. Fill nothing.
If you want to use transparent image for reg. Fill nothing in class.
"""
# text align left
description_label = tk.Label(root, text=description, justify=tk.LEFT)
description_label.grid(row=8, column=0, columnspan=3, sticky="w")

# identifier
identifier_label = tk.Label(root, text="Identifier")
identifier_label.grid(row=9, column=0, sticky="w")
identifier_var = tk.StringVar(value="")
identifier_entry = tk.Entry(root, textvariable=identifier_var)
identifier_entry.grid(row=9, column=1)

# class
class_label = tk.Label(root, text="Class")
class_label.grid(row=10, column=0, sticky="w")
class_var = tk.StringVar(value="")
class_entry = tk.Entry(root, textvariable=class_var)
class_entry.grid(row=10, column=1)

# regularization images count
reg_count_label = tk.Label(root, text="Regularization images count")
reg_count_label.grid(row=11, column=0, sticky="w")
reg_count_var = tk.IntVar(value=-1)
reg_count_entry = tk.Entry(root, textvariable=reg_count_var)
reg_count_entry.grid(row=11, column=1)

# run options
run_options_label = tk.Label(root, text="Run Options")
run_options_label.grid(row=12, column=0, sticky="w")
sd_path_label = tk.Label(root, text="StableDiffusion model path")
sd_path_label.grid(row=13, column=0, sticky="w")
sd_path_var = tk.StringVar(value="")
sd_path_entry = tk.Entry(root, textvariable=sd_path_var)
sd_path_entry.grid(row=13, column=1)
sd_path_button = tk.Button(root, text="Browse", command=lambda: sd_path_entry.insert(0, filedialog.askopenfilename()))
sd_path_button.grid(row=13, column=2)

model_output_dir_label = tk.Label(root, text="Model output directory")
model_output_dir_label.grid(row=14, column=0, sticky="w")
model_output_dir_var = tk.StringVar(value="")
model_output_dir_entry = tk.Entry(root, textvariable=model_output_dir_var)
model_output_dir_entry.grid(row=14, column=1)
model_output_dir_button = tk.Button(root, text="Browse", command=lambda: model_output_dir_entry.insert(0, filedialog.askdirectory()))
model_output_dir_button.grid(row=14, column=2)

model_output_name_label = tk.Label(root, text="Model output name")
model_output_name_label.grid(row=15, column=0, sticky="w")
model_output_name_var = tk.StringVar(value="")
model_output_name_entry = tk.Entry(root, textvariable=model_output_name_var)
model_output_name_entry.grid(row=15, column=1)

def get_values():
    return {
        "src": os.path.abspath(src_entry.get()),
        "dst": os.path.abspath(dst_entry.get()),
        "steps": steps_var.get(),
        "batch_size": batch_var.get(),
        "learning_rate": learning_rate_var.get(),
        "enable_bucket": enable_bucket_var.get(),
        "training_type": training_type_var.get(),
        "identifier": identifier_var.get(),
        "class": class_var.get(),
        "reg_count": reg_count_var.get(),
        "sd_path": os.path.abspath(sd_path_entry.get()),
        "model_output_dir": os.path.abspath(model_output_dir_entry.get()),
        "model_output_name": model_output_name_entry.get(),
    }

def run():
    values = get_values()

    # setup datasets
    src_img_dst = os.path.join(values["dst"], "target")
    tagimg.tagimg(values["src"], src_img_dst)

    # generate regularization images
    if values["training_type"] in ["class+identifier", "caption+class(dreambooth)"]:
        reg_img_dst = os.path.join(values["dst"], "reg")
        reg_count = values["reg_count"] if values["reg_count"] > 0 else len(tagimg.find_images(src_img_dst))
        os.makedirs(reg_img_dst, exist_ok=True)
        if values["class"] == "":
            gen_transparent.generate_images(reg_img_dst, reg_count)
        else:
            genregression.gen_img_diffusers(values["sd_path"], [values["class"]], reg_img_dst, reg_count)
    
    # generate config.toml
    toml = f"""[general]
enable_bucket = {"true" if values["enable_bucket"] else "false"}

[[datasets]]
resolution = 512
batch_size = {values["batch_size"]}

    [[datasets.subsets]]
    image_dir = '{src_img_dst}'
    num_repeats = 10
"""
    if values["training_type"] == "class+identifier":
        toml += f"""    class_tokens = '{values["class"]}, {values["identifier"]}'
"""
    elif values["training_type"] == "caption+class(dreambooth)":
        toml += """    caption_extension = '.caption'
"""
    else:
        toml += f"""    metadata_file = '{os.path.join(src_img_dst, "meta_clean.json")}'
"""

    if values["training_type"] in ["class+identifier", "caption+class(dreambooth)"]:
        toml += f"""
    [[datasets.subsets]]
    is_reg = true
    image_dir = '{reg_img_dst}'
    class_tokens = '{values["class"]}'
    num_repeats = 1
"""
    with open(os.path.join(values["dst"], "config.toml"), "w", encoding="utf-8") as f:
        f.write(toml)
    
    # setup execution script
    script = f"""accelerate launch --num_cpu_threads_per_process 1 train_network.py
--pretrained_model_name_or_path={values["sd_path"]}
--dataset_config={os.path.join(values["dst"], "config.toml")}
--output_dir={values["model_output_dir"]}
--output_name={values["model_output_name"]}
--save_model_as=safetensors
--prior_loss_weight=1.0
--max_train_steps={values["steps"]}
--learning_rate={values["learning_rate"]}
--optimizer_type="AdaFactor"
--optimizer_args "relative_step=True" "scale_parameter=True" "warmup_init=True"
--mixed_precision="fp16"
--cache_latents
--gradient_checkpointing
--network_module=networks.lora
--sample_every_n_steps=500
--sample_prompts={list(glob(os.path.join(src_img_dst, "*.caption")))[0]}
--sample_sampler=ddim
"""
    script = (" ").join(script.splitlines())
    with open(os.path.join(values["dst"], "run.sh"), "w", encoding="utf-8") as f:
        f.write(script)
    # exit app
    root.destroy()

# run button
run_button = tk.Button(root, text="Run", command=run)
run_button.grid(row=16, column=0, columnspan=3)

root.mainloop()