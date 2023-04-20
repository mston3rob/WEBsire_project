from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField, FieldList, FormField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired


class TestGenerateForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    to_who = StringField('Для кого', validators=[DataRequired()])
    count = StringField('Количество заданий', validators=[DataRequired()])
    one_answer = BooleanField('Только один ответ')
    go_out_btn = SubmitField('Вернуться', render_kw={'formnovalidate': True})
    create_test = SubmitField('Создать тест')
