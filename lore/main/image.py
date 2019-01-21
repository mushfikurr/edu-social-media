from PIL import Image
from flask import current_app
from secrets import token_hex
from os import path


def resize_and_save_post(input_picture, new_res):
    """
    Takes in and size and resizes to
    given size and outputs file name.
    """
    random_hex = token_hex(8)
    _, f_ext = path.splitext(input_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = path.join(
        current_app.root_path, 'static/img/posted', picture_fn)

    i = Image.open(input_picture)

    if i.size[0] == new_res[0] and i.size[1] == new_res[1]:
        return picture_fn

    scaled_res = (new_res[0]*2, new_res[1]*2)
    i.thumbnail(scaled_res)
    w, h = i.size[0], i.size[1]
    i = i.crop((w//2 - new_res[0]//2, h//2 - new_res[1]//2, w//2 + new_res[0]//2, h//2 + new_res[1]//2))
    i.save(picture_path, optimize=True, quality=85)

    return picture_fn

