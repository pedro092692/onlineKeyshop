from flask import render_template, redirect, url_for
from app.blueprints.security import bp
from app.forms.login import LoginForm
from app.forms.register import RegisterForm
from app.models.user import User
from app.extensions import generate_password_hash, check_password_hash, login_user

@bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data

        user = User.find_user(email=email)
        if user:
            # login and check password
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('main.home'))
        else:
            print('Invalid Password or user')

    return render_template('security/login.html', form=login_form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        email = register_form.email.data
        password = register_form.password.data
        confirm_password = register_form.confirm_password.data

        user = User.find_user(email=email)
        if not user:
            User.add_new_user(
                username=email,
                password=generate_password_hash(password=password, method='pbkdf2:sha256', salt_length=8)
            )
            return redirect(url_for('security.login'))
        else:
            print('this user already has been taken')


    return render_template('security/register.html', form=register_form)
