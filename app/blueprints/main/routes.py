from flask import render_template, redirect, url_for
from app.forms.login import LoginForm
from app.extensions import logout_user
from app.blueprints.main import bp
from app.models.product import Product

@bp.route('/')
def home():
    login_form = LoginForm()
    latest_products = Product.latest_products()
    return render_template('index.html', form=login_form, last_products=latest_products)

@bp.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('main.home'))