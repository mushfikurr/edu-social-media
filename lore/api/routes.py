from lore import db, jwt
import os
from lore.main.models import User, RevokedToken
from flask import request, jsonify
from flask_jwt_extended import (jwt_required, create_access_token,
                                create_refresh_token, get_raw_jwt,
                                jwt_refresh_token_required,
                                get_jwt_identity)
from werkzeug.exceptions import BadRequest, Unauthorized
from functools import wraps

from lore.api import bp


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return RevokedToken.is_jti_blacklisted(jti)


def parse_fields(expected_fields):
    def field_decorator(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            data = request.json
            for field in expected_fields:
                if field not in data:
                    return BadRequest(
                        f"The required field, {field} is missing.")
            return func(*args, **kwargs)
        return func_wrapper
    return field_decorator


@bp.before_request
def authenticate():
    """
    Called before any route access.
    Checks for authentication. AUTH_TOKEN is hardcoded in config for now.
    """
    token = request.headers.get('token')
    AUTH_TOKEN = os.getenv('AUTH_TOKEN')

    if token is None:
        return Unauthorized('Please provide a token in header of request.')
    if token != AUTH_TOKEN:
        return Unauthorized('Incorrect token. Please provide a correct token in header of request.')


def get_user_info(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return BadRequest(f"The user, {user} does not exist.")
    user_data = {
        "uuid": user.id,
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "last_seen": user.last_seen,
        "about_me": user.about_me,
        "follower_count": user.followers.count(),
        "followed_count": user.followed.count()
    }
    return user_data


@bp.route('/register', methods=['POST'])
@parse_fields(['username', 'email', 'first_name', 'last_name', 'password'])
def register():
    data = request.json
    response_dict = {
        "response": "Successfully created the account.",
        "errors": []
    }

    query_username = User.query.filter_by(username=data['username']).first()
    if query_username:
        response_dict['errors'].append(
            {"username": "This username is already taken."}
        )
    query_email = User.query.filter_by(email=data['email']).first()
    if query_email:
        response_dict['errors'].append(
            {"email": "This email is already taken."}
        )
    if query_username or query_email:
        response_dict['response'] = "There was an error submitting your form."
        return jsonify(response_dict)

    new_user = User(
        username=data['username'],
        email=data['email'],
        first_name=data['first_name'],
        last_name=data['last_name']
    )
    print("New user: " + str(new_user))

    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=data['username'])
    refresh_token = create_refresh_token(identity=data['username'])
    response_dict['access_token'] = access_token
    response_dict['refresh_token'] = refresh_token

    return jsonify(response_dict)


@bp.route('/login', methods=['POST'])
@parse_fields(['username', 'password'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()

    if user is None:
        return jsonify({"response": f"User {data['username']} does not exist."}), 404

    if user.check_password(data['password']):
        access_token = create_access_token(identity=data['username'])
        refresh_token = create_refresh_token(identity=data['username'])
        return jsonify(
            {
                "response": f"Successfully logged in as {user.username}",
                "access_token": access_token,
                "refresh_token": refresh_token
            }
        )
    else:
        return jsonify({"response": "Incorrect credentials."}), 404


@bp.route('/logout', methods=['POST'])
@jwt_required
def logout():
    jti = get_raw_jwt()['jti']

    revoked_token = RevokedToken(jti=jti)
    revoked_token.add()
    return jsonify({'response': 'Token has been revoked.'})


@bp.route('/logout2', methods=['POST'])
@jwt_refresh_token_required
def revoke_refresh_token():
    jti = get_raw_jwt()['jti']
    revoked_token = RevokedToken(jti=jti)
    revoked_token.add()
    return jsonify({'response': 'Refresh token has been revoked'})


@bp.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh_token():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    return jsonify({'access_token': access_token})


@bp.route('/user', methods=['POST'])
@parse_fields(['username'])
def user_info():
    data = request.json
    return jsonify(get_user_info(data['username']))


@bp.route('/post', methods=['POST'])
@parse_fields(['username'])
def post():
    """
    TODO: Posts
    """
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user is None:
        return BadRequest('That user does not exist.')
    if user.posts is None:
        return BadRequest('That user does not have any posts.')
    print("Hello")
    posts = {}
    for post in user.posts:
        post[post.id] = {"body:": post.body, "publish_date": post.publish_date}
    print(posts)
    user_posts = {
        "posts": user.posts,
        "followed_posts:": user.followed_posts()
    }
    user_posts.update(get_user_info(data['username']))
    return "<h1>Hi</h1>"
