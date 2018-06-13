from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from lore.constants import SECRET_KEY

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lore.db' # Temporary database 
db = SQLAlchemy(app)

from lore import routes
