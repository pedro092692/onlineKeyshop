from flask import render_template, redirect, url_for
from app.forms.login import LoginForm
from app.extensions import logout_user
from app.blueprints.main import bp

@bp.route('/')
def home():
    login_form = LoginForm()
    return render_template('index.html', form=login_form)

@bp.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('main.home'))