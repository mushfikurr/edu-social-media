from flask import Blueprint

bp = Blueprint('auth', __name__)

from lore.auth import routes
