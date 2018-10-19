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
    i.thumbnail(new_res)
    i.save(picture_path)

    return picture_fn


def clean_avatar(user):
    if user.image_file != "default.png":
        print(current_app.root_path + '/static/profile-pictures/' + user.image_file)
        image_path = current_app.root_path + '/static/profile-pictures/' + user.image_file
        remove(image_path)
    if user.small_image_file != "default_8080.png":
        print(current_app.root_path + '/static/profile-pictures/' + user.small_image_file)
        image_path = current_app.root_path + '/static/profile-pictures/8080/' + user.small_image_file
        remove(image_path)
