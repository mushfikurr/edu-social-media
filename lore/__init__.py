from flask import Flask
from lore import constants

app = Flask(__name__)
app.config['SECRET_KEY'] = constants.SECRET_KEY

from lore import routes