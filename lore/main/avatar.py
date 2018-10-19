from flask import current_app
from secrets import token_hex
from os import path, remove
from PIL import Image


def resize_and_save(input_picture, new_res):
    """
    Takes input picture and size and resizes to
    given size and outputs file name.
    """
    random_hex = token_hex(8)
    _, f_ext = path.splitext(input_picture.filename)
    picture_fn = random_hex + f_ext
    if new_res == (80, 80):
        print("Created avatar")
        picture_path = path.join(
            current_app.root_path, 'static/profile-pictures/8080', picture_fn)
    else:
        print("Created profile picture")
        picture_path = path.join(
            current_app.root_path, 'static/profile-pictures', picture_fn)

    i = Image.open(input_picture)
    if i.size[0] == 200 and i.size[1] == 200:
        return picture_fn
    if i.size[0] == 80 and i.size[1] == 80:
        return picture_fn
    scaled_res = (new_res[0]*2, new_res[1]*2)
    i.thumbnail(scaled_res)
    w, h = i.size[0], i.size[1]
    print(w, h)
    i = i.crop((w//2 - new_res[0]//2, h//2 - new_res[1]//2, w//2 + new_res[0]//2, h//2 + new_res[1]//2))
    print(i.size)
    i.save(picture_path)

    return picture_fn


def clean_avatar(user):
    if user.image_file != "default.png":
        image_path = path.join(
            current_app.root_path,
            'static/profile-pictures',
            user.image_file
        )
        print(current_app.root_path)
        print(image_path)
        print(path.exists(image_path))
        if path.exists(image_path):
            print(f"REMOVING: {image_path}")
            remove(image_path)
            user.image_file = "default.png"
        else:
            user.image_file = "default.png"
    if user.small_image_file != "default_8080.png":
        small_image_path = path.join(
            current_app.root_path,
            'static/profile-pictures/8080',
            user.small_image_file
        )
        if path.exists(small_image_path):
            print(f"REMOVING: {small_image_path}")
            remove(small_image_path)
            user.small_image_file = "default_8080.png"
        else:
            user.small_image_file = "default_8080.png"
