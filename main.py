from flask import Flask, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from flask import Flask, request, render_template
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from data import db_session
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from data import users, groups
import datetime
import random
import string


User = users.User
Group = groups.Group

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)

login_manager = LoginManager()
login_manager.init_app(app)

def generatePasswordToUsers():
    db_sess = db_session.create_session()
    password = ''
    a = string.ascii_lowercase + string.ascii_uppercase + '1234567890'
    for i in range(10):
        password += random.choice(a)
    exist = db_sess.query(User).filter(User.hashed_password == generate_password_hash(password)).first()
    while exist:
        for i in range(10):
            password += random.choice(a)
        exist = db_sess.query(User).filter(User.hashed_password == generate_password_hash(password)).first()
    return password

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


class GroupAppend(FlaskForm):
    initials = StringField('Введите всех учеников одной группы/класса в формате ФИО', validators=[DataRequired()])
    login = StringField('Введите логин группы', validators=[DataRequired()])
    name_group = StringField('Введите название группы', validators=[DataRequired()])
    submit = SubmitField('Создать группу')
    quantity = 1
    delete = SubmitField(label='Убрать', render_kw={'formnovalidate': True})
    add = SubmitField(label='Добавить +', render_kw={'formnovalidate': True})


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == form.login.data).first()
        if user and check_password_hash(user.hashed_password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            if current_user.teacher:
                return redirect("/listtestst") # редирект на страницу с тестами для учителя
            else:
                return redirect("/listtestss") # редирект на страницу с тестами для ученика (меняется последняя буква)
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/class_generate', methods=['GET', 'POST'])
@login_required
def class_generate():
    form = GroupAppend()
    if form.add.data:
        form.quantity += 1
    if form.submit():
        if form.initials.data:
            db_sess = db_session.create_session()
            a = form.initials.data
            if len(a.split(',')) > 1:
                separator = ','
            else:
                separator = '\r\n'
            login = form.login.data
            name_group = form.name_group.data
            group = Group()
            group.id_teacher = current_user.id
            group.login_group = login
            group.name_group = form.name_group.data

            db_sess.add(group)
            db_sess.commit()

            for i in a.split(separator):
                user = User()
                user.initials = i.strip()
                user.hashed_password = generate_password_hash(generatePasswordToUsers())
                user.teacher = False
                user.login = form.login.data
                user.hashed_key_access = None

                db_sess.add(user)
                db_sess.commit()
            return redirect('/listtestst')
    return render_template('class_generate.html', title='Создаие группы', form=form)


@app.route('/listtestst', methods=['GET', 'POST'])
@login_required
def listtestst():
    if current_user.teacher:
        return render_template('teacher_home.html')
    else:
        return 'access denied'


@app.route('/listtestss', methods=['GET', 'POST'])
@login_required
def listtestss():
    if current_user.teacher:
        return 'access denied'
    else:
        return 'now u are student'


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if form.password.data == form.confirm_password.data:
            user = User()
            user.initials = form.name.data
            user.hashed_password = generate_password_hash(form.password.data)
            user.teacher = True
            user.login = form.login.data
            user.hashed_key_access = None
            db_sess = db_session.create_session()
            db_sess.add(user)
            db_sess.commit()
            return redirect('/login')
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