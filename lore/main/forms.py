from flask_wtf import FlaskForm
from lore.main.models import User
from wtforms import StringField, SubmitField, TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import (DataRequired, Length, Email,
                                ValidationError)
from flask_login import current_user


class UpdateAccountForm(FlaskForm):
    """
    Form used for updating account details
    """
    # Validators
    name_validator = [DataRequired(), Length(max=256)]
    # All fields
    username = StringField(
        'Username',
        validators=[DataRequired(), Length(min=3, max=16)]
    )
    picture = FileField(
        'Upload Picture',
        validators=[FileAllowed(['jpg', 'png'])]
    )
    about_me = TextAreaField(
        'About Me',
        validators=[Length(max=120)]
    )
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()]
    )
    submit = SubmitField('Update')

    # Custom Validation
    def validate_username(self, username):
        """
        A custom validation error.
        This validation is for when a username is taken.
        """
        if username.data != current_user.username:
            query_user = User.query.filter_by(username=username.data).first()
            if query_user:
                print('failed username validation')
                raise ValidationError(
                    'That username is taken. Please try another one.'
                )

    def validate_email(self, email):
        """
        A custom validation error.
        This validation is for when a email is taken.
        """
        if email.data != current_user.email:
            query_user = User.query.filter_by(username=email.data).first()
            if query_user:
                print('failed email validation')
                raise ValidationError(
                    'That email address is taken. Please try another one.'
                )


class PostForm(FlaskForm):
    """
    Form used for submitting a post.
    """
    body = TextAreaField(
        'Say something...',
        validators=[DataRequired(), Length(min=1, max=140)]
    )
    submit = SubmitField('Submit')


class PostPictureForm(FlaskForm):
    """
    Form used for submitting a post with a picture.
    """
    caption = TextAreaField(
        'Caption your picture!',
        validators=[DataRequired(), Length(min=1, max=140)]
    )
    picture = FileField(
        'Attach a picture',
        validators=[FileAllowed(['jpg', 'png'])]
    )
    submit = SubmitField('Submit')


class TeacherPostForm(FlaskForm):
    """
    Form used for teacher resource uploading.
    """
    pass


class MessageForm(FlaskForm):
    """
    Form used to send a private message to a user.
    """
    message = TextAreaField(
        'Start a conversation',
        validators=[DataRequired(), Length(min=1, max=140)]
    )
    submit = SubmitField('Send')


class TaskForm(FlaskForm):
    """
    Form used to create a new task on a checklist.
    """
    task_title = StringField(
        'Title',
        validators=[DataRequired(), Length(1, 60)]
    )
    task_description = StringField(
        'Description',
        validators=[DataRequired(), Length(1, 128)]
    )
