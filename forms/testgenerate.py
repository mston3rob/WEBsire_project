from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField, FieldList, FormField, SelectField, IntegerField, TimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired


class TestGenerateForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    to_who = StringField('Укажите группу для которой предназначен тест', validators=[DataRequired()])
    count = IntegerField('Количество заданий', validators=[DataRequired()])
    go_out_btn = SubmitField('Вернуться', render_kw={'formnovalidate': True})
    time_to_test = IntegerField('Время на выполнение теста', validators=[DataRequired()])
    ed_izm = SelectField('Еденицы измерения', coerce=int, choices=[
        (0, 'Ч'),
        (1, 'М'),
        (2, 'С')
    ])