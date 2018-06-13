import json


def load_config():
    """
    Loads JSON file - config.json
    """
    with open('lore/config.json') as json_file:
        config = json.load(json_file)
        return config


# Auth Keys/Secrets
SECRET_KEY = load_config()["flask"]["secret-key"]
