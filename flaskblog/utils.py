import os
import secrets
from PIL import Image
from flask import current_app

ALLOWED_IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}

def save_image(form_picture, folder: str, output_size=(800, 800)) -> str:
    _, ext = os.path.splitext(form_picture.filename.lower())
    if ext not in ALLOWED_IMAGE_EXTS:
        raise ValueError("Invalid image type. Please upload jpg, jpeg, png, or webp.")

    random_hex = secrets.token_hex(8)
    picture_fn = random_hex + ext
    picture_path = os.path.join(current_app.root_path, "static", folder, picture_fn)

    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)

    return picture_fn
