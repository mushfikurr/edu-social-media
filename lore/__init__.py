from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from lore.config import Config
from flask_jwt_extended import JWTManager

# App start & config
app = Flask(__name__, static_url_path='/static')
app.config.from_object(Config)

# Database
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# Bcrypt
bcrypt = Bcrypt(app)

# Login Manager
login = LoginManager(app)
login.login_view = 'login'
login.login_message_category = 'info'


from lore import routes
