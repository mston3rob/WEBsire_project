from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField, FieldList, FormField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired


class TaskGenerateForm(FlaskForm):
    do_test_task = SubmitField('Сделать тест', render_kw={'formnovalidate': True})
    task_conditions = FieldList(StringField('Условие'), validators=[DataRequired()])
    go_out_btn = SubmitField('Вернуться', render_kw={'formnovalidate': True})