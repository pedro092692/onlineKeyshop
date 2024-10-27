from flask import render_template, redirect, url_for
from app.forms.admin.add_products import AddProduct
from app.forms.admin.add_category_form import AddCategory as SimpleForm
from app.models.category import Category
from app.blueprints.admin import bp



@bp.route('/')
def index():
    return render_template('admin/index.html')

# products
@bp.route('/products')
def products():
    return render_template('admin/products/index.html')

@bp.route('/add-product')
def add_product():
    form = AddProduct()
    return render_template('admin/products/add-product.html', form=form)


# categories
@bp.route('/categories')
def categories():
    # Category.add_category_form.py('playstore')
    return render_template('admin/categories/index.html')

@bp.route('/add-category', methods=['GET', 'POST'])
def add_category():
    form = SimpleForm()
    if form.validate_on_submit():
        category_name = form.name.data
        Category.add_category(Category, category_name)
        return redirect(url_for('admin.categories'))
    return render_template('admin/categories/add-category.html', form=form)


#subcategories
@bp.route('/subcategories')
def subcategories():
    return render_template('admin/subcategories/index.html')

@bp.route('/add-subcategories')
def add_subcategory():
    return render_template('admin/subcategories/add-subcategory.html')

#platforms
@bp.route('/platforms')
def platforms():
    form = SimpleForm()
    return render_template('admin/platforms/index.html', form=form)

@bp.route('/add-platform')
def add_platform():
    return render_template('admin/platforms/add-platform.html')

#keys
@bp.route('/keys')
def keys():
    return render_template('admin/keys/index.html')

@bp.route('/add-key')
def add_key():
    return render_template('admin/keys/add-key.html')
