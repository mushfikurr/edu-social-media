from lore import db, login, bcrypt
from datetime import datetime
from flask import url_for, current_app
from flask_login import UserMixin
from PIL import Image
import secrets
import os


@login.user_loader
def load_user(user_id):
    """
    Flask Login callback to get User session
    """
    return User.query.get(int(user_id))


followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class User(db.Model, UserMixin):
    """
    User model for DB
    Inherits from Flask Login's UserMixin
    """
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier
    username = db.Column(db.String(16), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.png')
    first_name = db.Column(db.String(256), nullable=False)
    last_name = db.Column(db.String(256), nullable=False)
    password = db.Column(db.String(60))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    about_me = db.Column(db.String(200))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    # Users that user has followed
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )

    def set_picture(self, uploaded_picture):
        """
        Sets the users picture after resizing.
        Saves locally in static/profile-pictures.
        """
        random_hex = secrets.token_hex(8)
        _, f_ext = os.path.splitext(uploaded_picture.filename)
        picture_fn = random_hex + f_ext
        picture_path = os.path.join(
            current_app.root_path,
            'static/profile-pictures',
            picture_fn
        )

        output_size = (125, 125)
        i = Image.open(uploaded_picture)
        i.thumbnail(output_size)
        i.save(picture_path)

        self.image_file = picture_fn
        print(self.image_file)
        print("SET PICTURE")
        db.session.commit()

    def set_email(self, new_email):
        """
        Sets the users email.
        Updates the user's email stored locally in DB.
        """
        self.email = new_email
        db.session.commit()

    def set_username(self, new_username):
        """
        Sets the users username.
        Updates the user's username stored locally in DB.
        """
        self.username = new_username
        db.session.commit()

    def set_password(self, original):
        """
        Hashes password and stores it.
        """
        self.password = bcrypt.generate_password_hash(original).decode('utf-8')
 
    def get_image_path(self):
        return url_for('static', filename='profile-pictures/' + self.image_file)

    def check_password(self, to_compare):
        """
        Checks input against hashed password
        """
        return bcrypt.check_password_hash(self.password, to_compare)

    def follow(self, user):
        """
        Follows given user
        """
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        """
        Unfollows given user
        """
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        """
        Low level query.
        Checks if assosciation table with left side foreign key is set to self
        user, and right side set to the user argument.
        Can return either 0 or 1 - NOT following or IS following.
        """
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        """
        Returns followed users and own posts in a timeline fashion
        """
        followed = Post.query.join(
            followers,
            (followers.c.followed_id == Post.author_id)
        ).filter(followers.c.follower_id == self.id)
        self_posts = Post.query.filter_by(author_id=self.id)
        return followed.union(self_posts).order_by(Post.publish_date.desc())

    def __repr__(self):
        """
        Displays how User model is printed
        """
        return f'User({self.username}, {self.email})'


class RevokedToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120), nullable=False)

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)


class Post(db.Model):
    """
    Model for a post that a user can have
    """
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(400), nullable=False)
    publish_date = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    # Foreign key to refer to User
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'Post({self.title}, {self.body}, {self.publish_date})'