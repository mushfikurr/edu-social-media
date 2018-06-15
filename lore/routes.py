from flask import render_template, redirect, url_for
from lore import app, db
from lore.forms import RegisterForm, LoginForm
from lore.models import User

# TODO: Integrate database (register a user, check if user in db, etc.)


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
    new_user = User(
        username=form_data['username'],
        email=form_data['email'],
        first_name=form_data['first_name'],
        last_name=form_data['last_name'],
        password=form_data['password']
    )
    db.session.add(new_user)
    db.session.commit()


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Endpoint for registering.
    """
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        on_register(register_form.data)
        return redirect(url_for('home'))
    else:
        print('user failed to register')
    return render_template(
        'register.html',
        form=register_form,
        title='Register'
    )


def on_login(form_data):
    """
    Fired when user logs in after passing validation.
    """
    username_input = form_data['username']
    password_input = form_data['password']
    user_query = User.query.filter_by(username=username_input).first()
    if user_query and user_query.password == password_input:
        print("user logged in successfully")
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
            on_login(login_form.data)
            return redirect(url_for('home'))
        except ValueError:
            print('Invalid credentials')
    else:
        print('user failed to login')
    return render_template(
        'login.html',
        form=login_form,
        title='Login'
    )
