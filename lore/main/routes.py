from flask import (render_template, redirect, url_for, flash, request,
                   current_app)
from flask_login import current_user, login_required
from lore import db
from lore.main.image import resize_and_save_post
from lore.main.avatar import resize_and_save
from lore.main import bp
from lore.main.forms import PostForm, PostPictureForm, UpdateAccountForm
from lore.main.models import User, Post, Message
from lore.main.avatar import clean_avatar
from datetime import datetime


@bp.before_request
def before_request():
    """
    Invoked before loading any view function.
    This is used for the last seen on user's profile.
    """
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route('/', methods=['GET', 'POST'])
def index():
    """
    Endpoint for index page.
    This shows followed posts and provides a form to create posts.
    """
    if current_user.is_authenticated:
        page = request.args.get('page', 1, type=int)
        posts = current_user.followed_posts().paginate(
            page,
            current_app.config['POSTS_PER_PAGE'],
            False
        )

        form = PostForm()
        pictureform = PostPictureForm()
        if form.validate_on_submit():
            if form.picture:
                print(form.picture.errors)
                picture_post = resize_and_save_post(form.picture.data)
                new_post = Post(body=form.body.data, author=current_user, picture=picture_post)
            else:
                new_post = Post(body=form.body.data, author=current_user)
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for('main.index'))

        next_url = url_for('main.index', page=posts.next_num) \
            if posts.has_next else None
        prev_url = url_for('main.index', page=posts.prev_num) \
            if posts.has_prev else None

        return render_template(
            'main/index.html',
            title="Home",
            posts=posts.items,
            next_url=next_url,
            prev_url=prev_url,
            form=form,
            pictureform=pictureform
        )
    else:
        return render_template('main/landing.html')


@bp.route('/explore')
def explore():
    """
    Endpoint for an explore page.
    Stream of users posts globally.
    """
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.publish_date.desc()).paginate(
        page,
        current_app.config['POSTS_PER_PAGE'],
        False
    )
    next_url = url_for('main.explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.explore', page=posts.prev_num) \
        if posts.has_prev else None

    return render_template(
        'main/explore.html',
        title='Explore',
        posts=posts.items,
        next_url=next_url,
        prev_url=prev_url
    )


@bp.route('/follow/<username>')
def follow(username):
    """
    Endpoint for following users.
    Allows a user to follow another user, recieving posts from them on index.
    The process behind following is explained @lore.models.User
    """
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('main.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('main.user', username=username))


@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    """
    Endpoint for unfollowing users.
    Allows a user to unfollow another user, no longer recieving posts from
    specified user.
    """
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('main.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('main.user', username=username))


@bp.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    """
    Profile for individual users.
    Can see their own posts and edit their information.
    """
    user = User.query.filter_by(username=username).first_or_404()

    # Update Account Form
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            clean_avatar(current_user)
            picture_file = resize_and_save(form.picture.data, (200, 200))
            small_picture_file = resize_and_save(form.picture.data, (80, 80))

            current_user.image_file = picture_file
            current_user.small_image_file = small_picture_file

        current_user.email = form.email.data
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()

        flash('Your account has been updated!', 'success')
        return redirect(url_for('main.user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me

    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.publish_date.desc()).paginate(
        page,
        current_app.config['POSTS_PER_PAGE'],
        False
    )

    next_url = url_for('main.user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    return render_template(
        'main/user.html',
        user=user,
        form=form,
        posts=posts.items,
        next_url=next_url,
        prev_url=prev_url
    )


@bp.route('/inbox')
def inbox():
    """
    Inbox for the user
    Uses @message model.
    """
    current_user.last_msg_read_time = datetime.utcnow()
    db.session.commit()

    page = request.args.get('page', 1, type=int)
    messages = current_user.messages_recieved.order_by(
        Message.timestamp.desc()).paginate(
            page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.messages', page=messages.next_num) \
        if messages.has_next else None
    prev_url = url_for('main.messages', page=messages.prev_num) \
        if messages.has_prev else None
    return render_template(
        'main/inbox.html',
        messages=messages.items,
        next_url=next_url,
        prev_url=prev_url,
        title="Inbox"
    )


@bp.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    return render_template(
        'main/search.html'
    )
