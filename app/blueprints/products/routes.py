from flask import render_template
from app.blueprints.products import bp
from app.models.product import Product

@bp.route('/')
def index():
    all_products = Product.get_products()
    return render_template('products/index.html', products=all_products)


