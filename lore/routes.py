from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required, login_user, logout_user
from lore import app, db, bcrypt
from lore.forms import RegisterForm, LoginForm, PostForm
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
    Endpoint for homepage.
    """
    if current_user.is_authenticated:
        posts = current_user.followed_posts().all()
        form = PostForm()
        if form.validate_on_submit():
            new_post = Post(body=form.body.data, author=current_user)
            db.session.add(new_post)
            db.session.commit()
            flash('Couldn\'t have said it better myself!', 'success')
            return redirect(url_for('index'))
        return render_template('index.html', posts=posts, form=form)
    else:
        return render_template('landing.html')


@app.route('/about')
def about():
    """
    Endpoint for about page.
    """
    return render_template('about.html', title='About')


def on_register(form_data):
    """
    Fired when user passes all validation.
    """
    password = form_data['password']
    hashed = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(
        username=form_data['username'],
        email=form_data['email'],
        first_name=form_data['first_name'],
        last_name=form_data['last_name'],
        password=hashed
    )
    db.session.add(new_user)
    db.session.commit()
    flash('Account created', 'info')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Endpoint for registering.
    """
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        on_register(register_form.data)
        return redirect(url_for('index'))
    return render_template(
        'register.html',
        form=register_form,
        title='Register'
    )


@app.route('/follow/<username>')
def follow(username):
    """
    Endpoint for following users
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


@app.route('/account', methods=['GET', 'POST'])
@login_required
def edit_account():
    """
    Endpoint for editing account.
    Requires to be logged in.
    """
    print('post request rec')
    posts = current_user.posts
    return render_template('account.html', posts=posts)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts
    return render_template('user.html', user=user, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Endpoint for logging in.
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
    Cleans up 'Remember Me' session
    """
    logout_user()
    return redirect(url_for('index'))
