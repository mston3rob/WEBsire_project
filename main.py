from flask import Flask, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from flask import Flask, request, render_template
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField, FieldList, FormField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired
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
quantity = 2

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


def generateAccessKey():
    nums = '1234567890'
    key = ''
    for i in range(7):
        key += random.choice(nums)
    return key + random.choice(string.ascii_uppercase)


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


class B(FlaskForm):
    inits = StringField(validators=[DataRequired()])


class GroupAppend(FlaskForm):
    initials = FieldList(FormField(B), min_entries=0, label='Введите всех учеников одной группы/класса в формате ФИО')
    login = StringField('Введите логин группы', validators=[DataRequired()])
    name_group = StringField('Введите название группы', validators=[DataRequired()])
    submit = SubmitField('Создать группу')
    count = StringField('Введите количество учеников группы:', validators=[DataRequired()])
    refresh = SubmitField(label='Обновить', render_kw={'formnovalidate': True})


class PreGroupAppend(FlaskForm):
    count = StringField('Введите количество учеников группы:', validators=[DataRequired()])
    refresh = SubmitField(label='Обновить', render_kw={'formnovalidate': True})


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

flag = False

@app.route('/class_generate', methods=['GET', 'POST'])
@login_required
def class_generate():
    global GroupAppend
    global flag
    form = GroupAppend()
    form1 = PreGroupAppend()
    if form.refresh.data:
        if form.count.data:

            class GroupAppend(FlaskForm):
                initials = FieldList(FormField(B), min_entries=int(form.count.data), max_entries=int(form.count.data),
                                     label='Введите всех учеников одной группы/класса в формате ФИО')
                login = StringField('Введите логин группы', validators=[DataRequired()])
                name_group = StringField('Введите название группы', validators=[DataRequired()])
                submit = SubmitField('Создать группу')
                count = StringField('Введите количество учеников группы:', validators=[DataRequired()])
                refresh = SubmitField(label='Обновить', render_kw={'formnovalidate': True})

            form = GroupAppend()
            return render_template('class_generate.html', title='Создаие группы', form=form)

        else:
            return render_template('preClassGenerate.html', title='Создаие группы', form=form1)

    if request.method == 'POST':
        if form.validate:
            db_sess = db_session.create_session()
            listOfPasswords = []
            key = generateAccessKey()
            for i in form.initials.data:
                password = generatePasswordToUsers()
                listOfPasswords.append((i['inits'], password))
                user = User()
                user.initials = i['inits']
                user.hashed_password = generate_password_hash(password)
                user.teacher = False
                user.login = form.login.data
                user.hashed_key_access = None
                db_sess = db_session.create_session()
                db_sess.add(user)
                db_sess.commit()

            group = Group()
            group.login_group = form.login.data
            group.name_group = form.name_group.data
            group.id_teacher = current_user.id
            group.hashed_key_access = generate_password_hash(key)
            db_sess = db_session.create_session()
            db_sess.add(group)
            db_sess.commit()
            if listOfPasswords:
                if len(listOfPasswords) % 3 == 1:
                    listOfPasswords.append(('', ''), ('', ''))
                elif len(listOfPasswords) % 3 == 2:
                    listOfPasswords.append(('', ''))
                print(listOfPasswords)
                session['last_login_added'] = listOfPasswords
                session['key_access'] = key
                return redirect('/password_list')
    return render_template('preClassGenerate.html', title='Создаие группы', form=form1)


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


@app.route('/password_list', methods=['GET', 'POST'])
@login_required
def passList():
    return render_template('passwordsList.html', title='Парооли для группы', list=session['last_login_added'],
                           len=len(session['last_login_added']), key=session['key_access'])


@app.route('/')
def home():
    return '1'


def main():
    db_session.global_init("db/tests.db")
    app.run()


if __name__ == '__main__':
    main()

    