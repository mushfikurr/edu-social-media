from functools import wraps
from flask import jsonify, request, flash, redirect, url_for
from flask_login import current_user, login_required

from lore import db
from lore.main.forms import TaskForm
from lore.main.models import Task, User

from lore.api import bp


def parse_fields(expected_fields):
    def field_decorator(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            data = request.json
            for field in expected_fields:
                if field not in data:
                    response = f'Required field {field} not found.'
                    return jsonify({'response': response}), 404
            return func(*args, **kwargs)
        return func_wrapper
    return field_decorator


@bp.route('/task/add', methods=['POST'])
@login_required
def add_task():
    form = TaskForm(request.form)

    if form.validate_on_submit():
        print(form.data)
        user = User.query.filter_by(
            username=current_user.username).first_or_404()
        task = Task(
            title=form.task_title.data,
            description=form.task_description.data,
            author=user
        )
        db.session.add(task)
        db.session.commit()
        return jsonify({'response': 'Successfully added task.'}), 200
    else:
        print(form.errors)
        return jsonify({'response': 'There was an error processing your request.'}), 400


@bp.route('/tasks', methods=['GET'])
@login_required
def get_all_tasks():
    tasks = current_user.descending_tasks()
    task_list = []
    for task in tasks:
        temp_task = {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'publish_date': task.publish_date
        }
        task_list.append(temp_task)
    
    response = {
        'response': "Successfully retrieved all tasks.",
        'tasks': task_list
    }
    return jsonify(response), 200


@bp.route('/task/<int:id>', methods=['GET'])
@login_required
def get_task(id):
    task = Task.query.filter_by(id=id).first_or_404()
    task_info = {
        'id': id,
        'title': task.title,
        'description': task.description,
        'is_finished': task.is_finished
    }

    return jsonify(task_info)


@bp.route('/task/<int:id>/toggle', methods=['PUT'])
@login_required
def toggle_task(id):
    task = Task.query.filter_by(id=id).first_or_404()
    task.toggle()

    return jsonify({'response': id + ' is now ' + task.is_finished}), 202


@bp.route('/task/<int:id>/delete', methods=['DELETE'])
@login_required
def delete_task(id):
    task = Task.query.filter_by(id=id).first_or_404()
    db.session.remove(task)
    db.session.commit()

    return jsonify({'response': 'Successfully removed task.'})