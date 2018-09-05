from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
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
    JWT_SECRET_KEY = 'JWT-SECRET-STRING'  # TODO: Change secret-string
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    SECRET_KEY = os.getenv("FLASK-SECRET-KEY")
    AUTH_TOKEN = os.getenv('AUTH_TOKEN')
    POSTS_PER_PAGE = 10