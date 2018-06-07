import json

def load_config():
    """
    Loads config into JSON format
    """
    with open('lore/config.json') as json_file:
        config = json.load(json_file)
        return config

SECRET_KEY = load_config()["flask"]["secret-key"]
