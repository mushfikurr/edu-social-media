from flask import Blueprint

bp = Blueprint('main', __name__)

from lore.main import routes
