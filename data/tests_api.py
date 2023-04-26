import flask
from flask import Flask, redirect, session, request, render_template, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField, FieldList, FormField, SelectField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired
from data import db_session, users, groups, groups_tests, tests
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
import datetime
import random
import string
from . import db_session
from .tests import Question
import json
import requests

User = users.User
Group = groups.Group
GroupTest = groups_tests.GroupTest
Question = tests.Question

blueprint = flask.Blueprint(
    'tests_api',
    __name__,
    template_folder='templates'
)


def init_flask_formB(entires_for_b=1, entires_for_a=1):
    class TestPost(FlaskForm):
        choosen_classes = FieldList(FormField(B), min_entries=entires_for_b, max_entries=entires_for_b)
        block_list = FieldList(FormField(A), min_entries=entires_for_a, max_entries=entires_for_a)
        submit = SubmitField('Опубликовать')

def init_flask_formA(entires):
    class TestPost(FlaskForm):
        choosen_classes = FieldList(FormField(B), min_entries=entires, max_entries=entires)


class A(FlaskForm):
    selected_student = RadioField()

class B(FlaskForm):
    selected_group = RadioField()

class TestPost(FlaskForm):
    choosen_groups = FieldList(FormField(B), min_entries=1)
    block_list = FieldList(FormField(A), min_entries=1)
    submit = SubmitField('Опубликовать')



@blueprint.route('/api/tests')
@login_required
def get_tests():
    db_sess = db_session.create_session()
    allTests = db_sess.query(GroupTest).filter(GroupTest.id_teacher == 1).all()
    return jsonify(
        {
            'tests':
                [item.to_dict(only=('id_teacher', 'id_group', 'id_questions', 'name'))
                 for item in allTests]
        }
    )

@blueprint.route('/api/tests_resp/<int:tests_id>', methods=['GET'])
@login_required
def get_test_for_response(tests_id):
    db_sess = db_session.create_session()
    allTests = db_sess.query(GroupTest).get(tests_id)
    if not allTests:
        return jsonify({'error': 'Not found1'})
    json_resp = jsonify(
        {
            'tests': allTests.to_dict(only=('id_teacher', 'id_group', 'id_questions', 'name'))
        }
    )
    return json_resp


@blueprint.route('/api/tests/<int:tests_id>/student/<int:student_id>')
@login_required
def get_result():
    pass


@blueprint.route('/test_sharing/<int:tests_id>', methods=['GET', 'POST'])
@login_required
def test_sharing(tests_id):
    global TestPost
    form = TestPost()
    response = requests.get(f'https://5f52-46-39-228-117.ngrok-free.app/api/tests_resp/{tests_id}')
    return render_template('test_sharing.html', form=form)


@blueprint.route('/api/tests/<int:tests_id>', methods=['GET'])
@login_required
def get_one_test(tests_id):
    db_sess = db_session.create_session()
    allTests = db_sess.query(GroupTest).get(tests_id)
    if not allTests:
        return jsonify({'error': 'Not found1'})
    json_resp = jsonify(
        {
            'tests': allTests.to_dict(only=('id_teacher', 'id_group', 'id_questions', 'name'))
        }
    )
    return render_template('testsReview.html', message=f'''Тест: "{json_resp.json['tests']['name'] }"''',
                           tests_id=tests_id)