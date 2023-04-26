from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField, FieldList, FormField, SelectField, IntegerField, TimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired


class DoTestForm(FlaskForm):
    answer = StringField('Ответ', validators=[DataRequired()])
    go_go = SubmitField('Следующий', render_kw={'formnovalidate': True})