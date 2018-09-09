from flask import Blueprint

bp = Blueprint('api', __name__)

from lore.api import routes