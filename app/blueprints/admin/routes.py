from flask import render_template
from app.forms.admin.add_products import AddProduct
from app.blueprints.admin import bp


@bp.route('/')
def index():
    return render_template('admin/index.html')

@bp.route('/products')
def products():
    return render_template('admin/products/index.html')

@bp.route('/add-product')
def add_product():
    form = AddProduct()
    return render_template('admin/products/add-product.html', form=form)
