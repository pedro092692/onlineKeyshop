from flask import render_template, redirect, url_for
from app.forms.login import LoginForm
from app.blueprints.main import bp
from app.models.product import Product

@bp.route('/')
def home():
    login_form = LoginForm()
    latest_products = Product.latest_products()
    return render_template('index.html', form=login_form, last_products=latest_products)

@bp.route('/product/<slug>')
def product(slug):
    product_item = Product.search_product_slug(slug)
    return render_template('product.html', product=product_item)

