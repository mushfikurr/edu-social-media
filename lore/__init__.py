from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from lore.constants import SECRET_KEY

# App initialisation
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

# Databse (Temporary)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lore.db'
db = SQLAlchemy(app)

# Bcrypt
bcrypt = Bcrypt(app)

# Login Manager
login = LoginManager(app)
login.login_view = 'login'
login.login_message_category = 'info'

from lore import routes
