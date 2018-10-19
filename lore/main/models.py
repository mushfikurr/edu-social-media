from lore import db, login, bcrypt
from datetime import datetime
from flask import url_for, current_app
from flask_login import UserMixin


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
    small_image_file = db.Column(db.String(20), nullable=False,
                           default='default_8080.png')
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    about_me = db.Column(db.String(120))
    last_msg_read_time = db.Column(db.DateTime)

    # Relationships with other tables
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    tasks = db.relationship('Task', backref='author', lazy='dynamic')
    messages_sent = db.relationship(
        'Message',
        foreign_keys='Message.sender_id',
        backref='author',
        lazy='dynamic'
    )
    messages_recieved = db.relationship(
        'Message',
        foreign_keys='Message.recipient_id',
        backref='recipient',
        lazy='dynamic'
    )
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )

    def set_password(self, original):
        """
        Hashes password and stores it.
        """
        self.password = bcrypt.generate_password_hash(original).decode('utf-8')
    
    def get_small_image_path(self):
        return url_for(
            'static', filename='profile-pictures/8080/' + self.small_image_file)

    def get_image_path(self):
        return url_for(
            'static', filename='profile-pictures/' + self.image_file)

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

    def descending_tasks(self):
        """
        Returns users tasks in descending order
        """
        tasks = self.tasks.order_by(Task.publish_date.desc()).all()
        return tasks

    def new_messages(self):
        """
        Returns a count of how many new messages a user has.
        """
        last_read_time = self.last_msg_read_time or datetime(1900, 1, 1)
        return Message.query.filter_by(recipient=self).filter(
            Message.timestamp > last_read_time).count()

    def __repr__(self):
        """
        Displays how User model is printed
        """
        return f'User({self.username}, {self.email})'


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return 'Message({})'.format(self.body)


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
        return f'Post({self.body}, {self.publish_date})'


class Task(db.Model):
    """
    Task model for DB
    Used for 'Checklist' function
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(128))
    is_finished = db.Column(db.Boolean, default=False)
    publish_date = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    # Foreign Key
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'Checklist({self.title}, {self.description}, {self.publish_date})'

    def toggle(self):
        if self.is_finished:
            self.is_finished = False
        else:
            self.is_finished = True
        db.session.commit()
