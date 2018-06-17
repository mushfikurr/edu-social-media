from lore import db, login
from datetime import datetime
from flask_login import UserMixin


@login.user_loader
def load_user(user_id):
    """
    Flask Login callback to get User session
    """
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """
    User model for DB
    Inherits from Flask Login's UserMixin
    """
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier
    username = db.Column(db.String(16), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(256), nullable=False)
    last_name = db.Column(db.String(256), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f'User({self.username}, {self.email}, {self.first_name}, {self.last_name}, {self.password})'


class Post(db.Model):
    """
    Model for a post that a user can have
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), nullable=False)
    body = db.Column(db.String(200), nullable=False)
    publish_date = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )
    # Foreign key to refer to User
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'Post({self.title}, {self.body}, {self.publish_date})'
