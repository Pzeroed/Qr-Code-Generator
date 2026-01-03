import os
import re

def sanitize_filename(name):
    name = re.sub(r'[<>:"/\\|?*]', "", name)
    return name.strip() or "qr_code"

def get_unique_path(folder, filename):
    base, ext = os.path.splitext(filename)
    counter = 1
    path = os.path.join(folder, filename)
    while os.path.exists(path):
        path = os.path.join(folder, f"{base}_{counter}{ext}")
        counter += 1
    return path
