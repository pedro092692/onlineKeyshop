from flask import render_template
from app.forms.login import LoginForm

from app.main import bp

@bp.route('/')
def home():
    login_form = LoginForm()
    return render_template('index.html', form=login_form)

@bp.route('/pedro')
def pedro():
    return 'this is another route'