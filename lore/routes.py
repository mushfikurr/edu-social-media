from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required, login_user, logout_user
from lore import app, db, bcrypt
from lore.forms import RegisterForm, LoginForm, UpdateAccountForm
from lore.models import User, Post


@app.route('/')
@app.route('/home')
def home():
    """
    Endpoint for homepage.
    """
    return render_template('home.html', title='Home')


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
        return redirect(url_for('app.home'))
    return render_template(
        'register.html',
        form=register_form,
        title='Register'
    )


def on_edit(form):
    current_user.username = form.username.data
    current_user.email = form.email.data
    current_user.first_name = form.first_name.data
    current_user.last_name = form.last_name.data

    db.session.commit()
    print('on edit')


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    """
    Endpoint for acc page.
    Requires to be logged in.
    """
    print('post request rec')
    posts = current_user.posts
    form = UpdateAccountForm()

    if form.validate_on_submit():
        print('validated form')
        on_edit(form)
        return redirect(url_for('app.account'))
    elif request.method == 'GET':
        print('this is a get request')
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
    return render_template('account.html', form=form, posts=posts)


def on_login(form):
    """
    Fired when user logs in after passing validation.
    """
    form_data = form.data
    username_input = form_data['username']
    password_input = form_data['password']
    user_query = User.query.filter_by(username=username_input).first()
    if user_query and bcrypt.check_password_hash(user_query.password, password_input):
        login_user(user_query, remember=form.remember)
        flash('user logged in successfully', 'info')
    else:
        raise ValueError('Invalid credentials')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Endpoint for logging in.
    """
    login_form = LoginForm()
    if login_form.validate_on_submit():
        try:
            on_login(login_form)
            return redirect(url_for('app.home'))
        except ValueError:
            print('Invalid credentials')
    return render_template(
        'login.html',
        form=login_form,
        title='Login'
    )


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    """
    Endpoint for logging user out.
    Cleans up 'Remember Me' session
    """
    logout_user()
    return redirect(url_for('app.home'))