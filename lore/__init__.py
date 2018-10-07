from flask import Flask
from flask_moment import Moment
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from lore.config import Config

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
csrf = CSRFProtect()
moment = Moment()

# Login Configuration
login = LoginManager()
login.login_view = 'auth.login'
login.login_message_category = 'info'


def create_app(config_class=Config):
    # App start & config
    app = Flask(__name__, static_url_path='/static')
    app.config.from_object(Config)

    # Blueprints
    from lore.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    print(" * Loaded Auth")
    from lore.main import bp as main_bp
    app.register_blueprint(main_bp)
    print(" * Loaded Main")
    from lore.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    print(" * Loaded API")

    # Database
    db.init_app(app)
    migrate.init_app(app, db)

    # Bcrypt
    bcrypt.init_app(app)

    # Login Manager
    login.init_app(app)

    # CSRF Protection
    csrf.init_app(app)

    # Moments
    moment.init_app(app)

    return app
