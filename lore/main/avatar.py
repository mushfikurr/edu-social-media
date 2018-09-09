from flask import current_app
from secrets import token_hex
from os import path
from PIL import Image


def resize_and_save(input_picture, new_res):
    """
    Takes input picture and size and resizes to 
    given size and outputs file name.
    """
    random_hex = token_hex(8)
    _, f_ext = path.splitext(input_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = path.join(
        current_app.root_path, 'static/profile-pictures', picture_fn)

    i = Image.open(input_picture)
    i.thumbnail(new_res)
    i.save(picture_path)

    return picture_fn
