from flask import render_template, redirect, url_for
from app.forms.admin.add_products import AddProduct
from app.forms.admin.add_category_form import AddCategory as SimpleForm
from app.forms.admin.add_subcategory_form import SubcategoryForm
from app.models.category import Category
from app.models.sub_category import SubCategory
from app.models.platforms import Platform
from app.models.product import Product
from app.models.key import Key
from app.models.product_keys import ProductKeys
from app.extensions import generate_password_hash
from app.blueprints.admin import bp



@bp.route('/')
def index():
    return render_template('admin/index.html')

# products
@bp.route('/products')
def products():
    return render_template('admin/products/index.html')

@bp.route('/add-product', methods=['GET', 'POST'])
def add_product():
    form = AddProduct()
    all_categories = Category.categories()
    all_subcategories = SubCategory.subcategories()
    all_platforms = Platform.platforms()

    form.product_category.choices = [(0, 'Select One')] + [(category.id, category.name) for category in all_categories]
    form.product_subcategory.choices = ([(0, 'Select One')] +
                                        [(subcategory.id, subcategory.name) for subcategory in all_subcategories])
    form.product_platform.choices = [(0, 'Select One')] + [(platform.id, platform.name) for platform in all_platforms]

    if form.validate_on_submit():
        #product infor
        product_name = form.product_name.data
        platform_id = form.product_platform.data
        category_id = form.product_category.data
        subcategory_id = form.product_subcategory.data
        #key info
        product_key =  generate_password_hash(password=form.product_key_code.data, method='pbkdf2:sha256', salt_length=8)
        product_price = form.product_price.data

        # add new product
        new_product = Product.add_product(Product, product_name, platform_id, category_id, subcategory_id)
        # add new key
        new_key = Key.add_key(Key, product_key, 0, product_price)
        # add new product key
        ProductKeys.add_new_product_key(ProductKeys, new_product.id, new_key.id)

        return redirect(url_for('admin.products'))



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

@bp.route('/add-platform', methods=['GET', 'POST'])
def add_platform():
    form = SimpleForm()
    # config form
    form.name.label = 'Platform Name'
    form.submit.label.text = 'Add Platform'

    if form.validate_on_submit():
        platform_name = form.name.data
        Platform.add_platform(Platform, platform_name)
        return redirect(url_for('admin.platforms'))

    return render_template('admin/platforms/add-platform.html', form=form)

#keys
@bp.route('/keys')
def keys():
    return render_template('admin/keys/index.html')

@bp.route('/add-key')
def add_key():
    return render_template('admin/keys/add-key.html')
