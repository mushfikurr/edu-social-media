from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required, login_user, logout_user
from lore import app, db
from lore.forms import RegisterForm, LoginForm, PostForm, UpdateAccountForm
from lore.models import User, Post
from datetime import datetime


@app.before_request
def before_request():
    """
    Invoked before loading any view function.
    This is used for the last seen on user's profile.
    """
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Endpoint for index page.
    This shows followed posts and provides a form to create posts.
    """
    if current_user.is_authenticated:
        page = request.args.get('page', 1, type=int)
        posts = current_user.followed_posts().paginate(
            page,
            app.config['POSTS_PER_PAGE'],
            False
        )

        form = PostForm()
        if form.validate_on_submit():
            new_post = Post(body=form.body.data, author=current_user)
            db.session.add(new_post)
            db.session.commit()
            flash("Couldn't have said it better myself!", 'success')
            return redirect(url_for('index'))

        next_url = url_for('index', page=posts.next_num) \
            if posts.has_next else None
        prev_url = url_for('index', page=posts.prev_num) \
            if posts.has_prev else None

        return render_template(
            'index.html',
            title="Home",
            posts=posts.items,
            next_url=next_url,
            prev_url=prev_url,
            form=form
        )
    else:
        return render_template('landing.html')


@app.route('/explore')
def explore():
    """
    Endpoint for an explore page.
    Stream of users posts globally.
    """
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.publish_date.desc()).paginate(
        page,
        app.config['POSTS_PER_PAGE'],
        False
    )
    next_url = url_for('index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) \
        if posts.has_prev else None

    return render_template(
        'index.html',
        title='Explore',
        posts=posts.items,
        next_url=next_url,
        prev_url=prev_url
    )


@app.route('/about')
def about():
    """
    Endpoint for about page.
    An about page explaining the motives of the website.
    """
    return render_template('about.html', title='About')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Endpoint for registering.
    Allows users to create an account, and is added into the database.
    """
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        new_user = User(
            username=register_form.username.data,
            email=register_form.email.data,
            first_name=register_form.first_name.data,
            last_name=register_form.last_name.data
        )
        new_user.set_password(register_form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created', 'info')
        return redirect(url_for('index'))
    return render_template(
        'register.html',
        form=register_form,
        title='Register'
    )


@app.route('/follow/<username>')
def follow(username):
    """
    Endpoint for following users.
    Allows a user to follow another user, recieving posts from them on index.
    The process behind following is explained @lore.models.User
    """
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('user', username=username))


@app.route('/unfollow/<username>')
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
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('user', username=username))


@app.route('/edit_account', methods=['GET', 'POST'])
@login_required
def edit_account():
    """
    Endpoint for editing account.
    NOTE: Not complete.
    """
    posts = current_user.posts
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            current_user.set_picture(form.picture.data)
        current_user.set_email(form.email.data)
        current_user.set_username(form.username.data)
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('edit_account.html', posts=posts, form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    """
    Profile for individual users.
    Can see their own posts and edit their information.
    """
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.publish_date.desc()).paginate(
        page,
        app.config['POSTS_PER_PAGE'],
        False
    )
    next_url = url_for('user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    return render_template(
        'user.html',
        user=user,
        posts=posts.items,
        next_url=next_url,
        prev_url=prev_url
    )


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Endpoint for logging in.
    Sessions handled by Flask-Login.
    """
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember.data)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    """
    Endpoint for logging user out.
    Sessions handled by Flask-Login.
    """
    logout_user()
    return redirect(url_for('index'))
