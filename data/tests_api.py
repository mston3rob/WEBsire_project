import flask
from flask import jsonify
from data import db_session, users, groups, groups_tests, tests
from . import db_session
from .tests import Question

User = users.User
Group = groups.Group
GroupTest = groups_tests.GroupTest
Question = tests.Question

blueprint = flask.Blueprint(
    'tests_api',
    __name__,
    template_folder='templates'
)

@blueprint.route('/api/tests')
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


@blueprint.route('/api/tests/<int:tests_id>', methods=['GET'])
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
    return json_resp