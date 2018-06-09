from flask import render_template, redirect, url_for
from lore import app, forms


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


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Endpoint for registering.
    """
    register_form = forms.RegisterForm()
    if register_form.validate_on_submit():
        print('user has registered')
        return redirect(url_for('home'))
    else:
        print('user failed to register')
    return render_template('register.html', form=register_form, title='Register')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Endpoint for logging in.
    """
    login_form = forms.LoginForm()
    if login_form.validate_on_submit():
        print('user has logged in')
        return redirect(url_for('home'))
    else:
        print('user failed to login')
    return render_template('login.html', form=login_form, title='Login')
