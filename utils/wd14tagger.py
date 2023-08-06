import os
import sys
import glob

import numpy as np
import onnxruntime as rt
import pandas as pd
from PIL import Image
import importlib
from utils.settings import BASE_DIR
from SW_CV_ModelZoo.Utils import dbimutils

dim = 448
thresh = 0.3771
model = rt.InferenceSession(os.path.join(BASE_DIR, "models", "wd14", "model.onnx"))
label_names = pd.read_csv(os.path.join(BASE_DIR, "models", "wd14", "selected_tags.csv "))

def read_image(path):
    img = Image.open(path).convert("RGB")
    r, g, b = img.split()
    img = Image.merge("RGB", (b, g, r))
    img = np.array(img)
    img = dbimutils.smart_24bit(img)
    img = dbimutils.make_square(img, dim)
    img = dbimutils.smart_resize(img, dim)
    img = img.astype(np.float32)
    img = np.expand_dims(img, 0)
    return img

def generate_tags(path):
    img = read_image(path)
    input_name = model.get_inputs()[0].name
    label_name = model.get_outputs()[0].name
    probs = model.run([label_name], {input_name: img})[0]
    label_names["probs"] = probs[0]
    found_tags = label_names[label_names["probs"] > thresh][["tag_id", "name", "probs"]]
    return found_tags["name"].tolist()
