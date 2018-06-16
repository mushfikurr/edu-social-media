from lore import db
from datetime import datetime

# TODO: Relationship between User and Posts


class User(db.Model):
    """
    User model for database
    """
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier
    username = db.Column(db.String(16), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(256), nullable=False)
    last_name = db.Column(db.String(256), nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return (
            f'User({self.username}',
            f'{self.email}',
            f'{self.first_name}',
            f'{self.last_name}',
            f'{self.password})'
        )


class Post(db.Model):
    """
    Model for a post that a user can have
    """
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(200), nullable=False)
    publish_date = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )
