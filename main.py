from flask import Flask, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from flask import Flask, request, render_template
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from data import db_session
from flask_login import LoginManager, login_user
from data import users

User = users.User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    name = StringField('ФИО', validators=[DataRequired()])
    login = StringField('Введите логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегестрироваться')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == form.login.data).first()
        if user and check_password_hash(user.hashed_password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if form.password.data == form.confirm_password.data:
            user = User()
            user.name = form.name.data.split()[1]
            user.surname = form.name.data.split()[0]
            user.patronymic = form.name.data.split()[2]
            user.hashed_password = generate_password_hash(form.password.data)
            user.teacher = True
            user.login = form.login.data
            db_sess = db_session.create_session()
            db_sess.add(user)
            db_sess.commit()
        else:
            return render_template('register_form.html',
                                   message="Пароли не совпадают",
                                   form=form)
    return render_template('register_form.html', title='Регистрация', form=form)


@app.route('/')
def home():
    return '1'


def main():
    db_session.global_init("db/tests.db")
    app.run()


if __name__ == '__main__':
    main()