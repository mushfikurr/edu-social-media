from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required, login_user, logout_user
from lore import app, db, bcrypt
from lore.forms import RegisterForm, LoginForm
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


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    """
    Endpoint for acc page.
    Requires to be logged in.
    """
    print('post request rec')
    posts = current_user.posts
    return render_template('account.html', posts=posts)


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

        login_user(user, remember=form.remember_me.data)
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
    return redirect(url_for('home'))
