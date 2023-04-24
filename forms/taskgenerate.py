from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField, FieldList, FormField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired


class TaskForm(FlaskForm):
    condition = StringField('Условие', validators=[DataRequired()])
    answers = StringField('Ответы', validators=[DataRequired()])
    true_answer = StringField('Верный ответ', validators=[DataRequired()])


class TaskGenerateForm(FlaskForm):
    do_test_task = SubmitField('Сделать тест', render_kw={'formnovalidate': True})
    tasks_list = FieldList(FormField(TaskForm), min_entries=100)