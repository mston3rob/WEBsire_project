from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FieldList, FormField, SelectField, IntegerField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired


class TaskAnswerForm(FlaskForm):
    answer = StringField('', validators=[DataRequired()])


class TaskForm(FlaskForm):
    condition = TextAreaField('Условие', validators=[DataRequired()])
    condition_file = FileField('Файл условия')
    answers = FieldList(FormField(TaskAnswerForm), min_entries=4)
    true_answer = StringField('Верный ответ', validators=[DataRequired()])
    type_answer = SelectField('Тип ответа', coerce=int, choices=[
        (1, 'Строка'),
        (2, 'Выбор из вариантов'),
        (3, 'Один выбор из вариантов')])
    cost = IntegerField('Количество баллов за задание', validators=[DataRequired()])



class TaskGenerateForm(FlaskForm):
    task_reset = SubmitField('Обновить страницу', render_kw={'formnovalidate': True})
    do_test_task = SubmitField('Сделать тест', render_kw={'formnovalidate': True})
    tasks_list = FieldList(FormField(TaskForm), min_entries=100)
