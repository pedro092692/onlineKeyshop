from flask import render_template, redirect, url_for
from app.forms.admin.add_products import AddProduct
from app.forms.admin.add_category_form import AddCategory as SimpleForm
from app.forms.admin.add_subcategory_form import SubcategoryForm
from app.models.category import Category
from app.models.sub_category import SubCategory
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

@bp.route('/add-subcategory', methods=['GET', 'POST'])
def add_subcategory():
    form = SubcategoryForm()
    categories_ = Category.categories()

    form.category_id.choices = [(0, 'Select One')] + [(category.id, category.name) for category in categories_]
    if form.validate_on_submit():
        subcategory_name = form.name.data
        category_id = form.category_id.data
        # add new subcategory
        SubCategory.add_subcategory(SubCategory, category_id, subcategory_name)
        return redirect(url_for('admin.subcategories'))
    return render_template('admin/subcategories/add-subcategory.html', form=form)

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
