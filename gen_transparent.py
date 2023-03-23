import os
import sys
from PIL import Image

def generate_transparent(path, h, w):
    # generate transparent image
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    img.save(path)

def generate_images(dir, n, h=512, w=512):
    # generate n transparent images
    for i in range(n):
        path = os.path.join(dir, f"{i}.png")
        generate_transparent(path, h, w)

def main():
    dir = os.path.abspath(sys.argv[1])
    n = int(sys.argv[2])
    generate_images(dir, n)
    