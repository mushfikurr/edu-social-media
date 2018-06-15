from lore import db


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
