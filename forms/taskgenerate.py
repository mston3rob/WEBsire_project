from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField, FieldList, FormField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired


class TaskGenerateForm(FlaskForm):
    pass