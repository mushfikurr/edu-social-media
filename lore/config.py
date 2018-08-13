from dotenv import load_dotenv
import os

# Loading dotenv config and getting base dir
load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """
    Config object for app config
    """
    DEBUG = True  # False when in production
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'lore.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("FLASK-SECRET-KEY")
    POSTS_PER_PAGE = 1
