from lore import db
from lore.main.models import User
from flask import redirect, url_for, flash, render_template
from flask_login import login_user, logout_user, login_required, current_user
from lore.auth.forms import RegisterForm, LoginForm

from lore.auth import bp


@bp.route('/login', methods=['GET', 'POST'])
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
            flash('Invalid username or password', 'danger')
            return redirect(url_for('auth.login'))

        login_user(user, remember=form.remember.data)
        return redirect(url_for('main.index'))
    return render_template('auth/login.html', form=form)


@bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    """
    Endpoint for logging user out.
    Sessions handled by Flask-Login.
    """
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
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
        flash('Account created successfully!', 'info')
        return redirect(url_for('auth.login'))
    return render_template(
        'register.html',
        form=register_form,
        title='Register'
    )
