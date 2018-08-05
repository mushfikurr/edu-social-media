from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from lore.config import Config

# App start & config
app = Flask(__name__)
app.config.from_object(Config)

# Database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Bcrypt
bcrypt = Bcrypt(app)

# Login Manager
login = LoginManager(app)
login.login_view = 'login'
login.login_message_category = 'info'

from lore import routes
