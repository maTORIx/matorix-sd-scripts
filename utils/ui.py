import typing
import tkinter as tk
from tkinter import ttk, filedialog


class UI:
    def __init__(self, cache: dict = None):
        self.root = tk.Tk()
        self.current_row = -1
        self.cache = cache or {}
        self.values = {}

    def get_values(self):
        return {k: v.get() for k, v in self.values.items()}

    def add_checkbox(self, text: str):
        self.current_row += 1
        label = tk.Label(self.root, text=text)
        label.grid(row=self.current_row, column=0, sticky="w")
        var = tk.BooleanVar(value=self.cache.get(text, False))
        checkbox = tk.Checkbutton(self.root, variable=var)
        checkbox.grid(row=self.current_row, column=1, sticky="w")
        self.values[text] = var
        return var

    def add_option_menu(self, text: str, options: typing.List[str]):
        self.current_row += 1
        options = [str(x) for x in options]
        label = tk.Label(self.root, text=text)
        label.grid(row=self.current_row, column=0, sticky="w")
        var = tk.StringVar(value=self.cache.get(text, options[0]))
        combobox = ttk.Combobox(
            self.root, textvariable=var, values=options, style="TCombobox"
        )
        combobox["values"] = options
        combobox.grid(row=self.current_row, column=1, sticky="w")
        self.values[text] = var
        return var

    def add_path_entry(self, text: str, dir=False):
        self.current_row += 1
        label = tk.Label(self.root, text=text)
        label.grid(row=self.current_row, column=0, sticky="w")
        var = tk.StringVar(value=self.cache.get(text, ""))
        entry = tk.Entry(self.root, textvariable=var)
        entry.grid(row=self.current_row, column=1, sticky="w")
        if dir:
            button = ttk.Button(
                self.root,
                text="Browse",
                command=lambda: var.set(filedialog.askdirectory()),
                style="TButton",
            )
        else:
            button = ttk.Button(
                self.root,
                text="Browse",
                command=lambda: var.set(filedialog.askopenfilename()),
                style="TButton",
            )
        button.grid(row=self.current_row, column=2)
        self.values[text] = var
        return var

    def add_entry(self, text: str, varType: str = "string", initialValue=None):
        self.current_row += 1
        label = tk.Label(self.root, text=text)
        label.grid(row=self.current_row, column=0, sticky="w")
        if varType == "int":
            if initialValue is None:
                initialValue = 0
            var = tk.IntVar(value=self.cache.get(text, initialValue))
        elif varType == "double":
            if initialValue is None:
                initialValue = 0.0
            print(initialValue)
            var = tk.DoubleVar(value=self.cache.get(text, initialValue))
        elif varType == "string":
            if initialValue is None:
                initialValue = ""
            var = tk.StringVar(value=self.cache.get(text, initialValue))
        else:
            raise ValueError(f"Invalid varType: {varType}")
        entry = tk.Entry(self.root, textvariable=var)
        entry.grid(row=self.current_row, column=1, sticky="w")
        self.values[text] = var
        return var

    def add_label(self, text: str):
        self.current_row += 1
        label = tk.Label(self.root, text=text)
        label.grid(row=self.current_row, column=0, sticky="w")

    def mainloop(self):
        self.root.mainloop()

    def destroy(self):
        self.root.destroy()


class CustomUI(UI):
    def __init__(self, cache, TRAINING_OPTIONS):
        super().__init__(cache)
        self.TRAINING_OPTIONS = TRAINING_OPTIONS

    def add_from_training_options(self, category: str, label: str):
        if (
            category not in self.TRAINING_OPTIONS
            or label not in self.TRAINING_OPTIONS[category]
        ):
            raise ValueError(f"Invalid category: {category} or label: {label}")
        option = self.TRAINING_OPTIONS[category][label]
        if category == "flags":
            self.add_checkbox(label)
        elif category == "values":
            self.add_entry(label, option["type"], option.get("default", None))
        elif category == "selects":
            self.add_option_menu(label, option["values"])
        elif category == "types":
            self.add_option_menu(label, option.keys())
        else:
            raise ValueError(f"Invalid category: {category}")


def setup_style():
    style = ttk.Style()
    style.configure(
        "TButton",
        width=20,
        height=20,
        borderwidth=1,
        relief="flat",
        background="white",
        foreground="black",
        font="Consolas 11",
        anchor="center",
    )
    style.configure(
        "TCombobox",
        width=20,
        borderwidth=1,
        relief="flat",
        background="white",
        foreground="black",
        font="Consolas 11",
        anchor="left",
    )


def setup_ui(cache, TRAINING_OPTIONS, run_func: typing.Callable):
    ui = CustomUI(cache, TRAINING_OPTIONS)
    ui.root.title("matroix-sd-scripts")
    ui.root.option_add("*Font", "Consolas 11")
    ui.root.option_add("*Background", "white")
    ui.root.configure(background="white")
    setup_style()

    ui.add_entry("Model Name")
    ui.add_checkbox("Is SDXL")
    ui.add_path_entry("Image Source Directory", dir=True)
    ui.add_path_entry("StableDiffusion Model Path")
    ui.add_path_entry("VAE Path")
    ui.add_label("Training options")
    ui.add_from_training_options("values", "steps")
    ui.add_entry("Batch Size", "int", 1)
    ui.add_option_menu("Image shape", ["square", "portrait", "landscape"])
    ui.add_entry("Identifier")
    ui.add_checkbox("Use Identifier Only")
    ui.add_entry("Class")
    ui.add_entry("Regularization images count", "int", 0)
    ui.add_from_training_options("selects", "sampler")
    ui.add_from_training_options("flags", "Train U-Net only")
    ui.add_from_training_options("flags", "Enable image ratio bucket")
    ui.add_from_training_options("flags", "Cache latents")
    ui.add_from_training_options("types", "network")
    ui.add_from_training_options("types", "optimizer")
    ui.add_from_training_options("flags", "torch 2.0")
    ui.add_from_training_options("flags", "xformers")
    ui.add_from_training_options("values", "Caption dropout rate")
    ui.add_from_training_options("selects", "max token length")
    ui.add_from_training_options("flags", "shuffle caption")
    ui.add_label("Augmentation")
    ui.add_from_training_options("flags", "Flip LR")
    ui.add_from_training_options("flags", "Color aug")
    ui.add_from_training_options("flags", "Random crop")

    # run button
    ui.current_row += 1
    run_button = ttk.Button(ui.root, text="Run", command=run_func, style="TButton")
    run_button.grid(row=ui.current_row, column=0, columnspan=3, sticky="e")
    return ui
