from flask import render_template, redirect, url_for
from app.forms.admin.add_products import AddProduct
from app.forms.admin.update_product_form import UpdateProduct
from app.forms.admin.add_category_form import AddCategory as SimpleForm
from app.forms.admin.add_subcategory_form import SubcategoryForm
from app.forms.admin.add_new_key_form import AddKey
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
    all_products = Product.get_products()
    return render_template('admin/products/index.html', products=all_products)

@bp.route('/add-product', methods=['GET', 'POST'])
def add_product():
    form = AddProduct()
    # fill dynamic form choices
    fill_form_product(form)

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

@bp.route('/product/<product_id>', methods=['GET', 'POST'])
def product_info(product_id):
    product = Product.get_product(product_id)
    form_product = UpdateProduct()
    # fill dynamic form choices
    fill_form_product(form_product)
    if form_product.submit.data and form_product.validate():
        product_name = form_product.name.data
        category_id = form_product.product_category.data
        subcategory_id = form_product.product_subcategory.data
        platform_id = form_product.product_platform.data
        # update product
        Product.update_product(product, product_name,
                               platform_id,
                               category_id,
                               subcategory_id
                               )
        return redirect(url_for('admin.products'))

    form_product.name.data = product.name
    form_product.product_category.data = product.category_id
    form_product.product_platform.data = product.platform_id
    form_product.product_subcategory.data = product.sub_category_id

    # new key product form
    form_key = AddKey()

    if form_key.submit.data and form_key.validate():
        product_key = form_key.key_value.data
        key_price = form_key.price.data
        # add new key
        new_key = Key.add_key(Key, product_key, 0, key_price)
        # add new product key
        ProductKeys.add_new_product_key(ProductKeys, product.id, new_key.id)
        return redirect(url_for('admin.products'))

    return render_template('admin/products/product.html', form=form_product, form_key=form_key,
                           product=product)

@bp.route('/product/delete/<product_id>', methods=['POST'])
def delete_product(product_id):
    product = Product.get_product(product_id)
    Product.delete_product(product)
    return redirect(url_for('admin.products'))


# categories
@bp.route('/categories')
def categories():
    all_categories = Category.categories()
    return render_template('admin/categories/index.html', categories=all_categories)

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
    all_subcategories = SubCategory.subcategories()
    return render_template('admin/subcategories/index.html', subcategories=all_subcategories)

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
    all_platforms = Platform.platforms()
    return render_template('admin/platforms/index.html', platforms=all_platforms)

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


def fill_form_product(form):
    all_categories = Category.categories()
    all_subcategories = SubCategory.subcategories()
    all_platforms = Platform.platforms()

    form.product_category.choices = [(0, 'Select One')] + [(category.id, category.name) for category in all_categories]
    form.product_subcategory.choices = ([(0, 'Select One')] +
                                        [(subcategory.id, subcategory.name) for subcategory in all_subcategories])
    form.product_platform.choices = [(0, 'Select One')] + [(platform.id, platform.name) for platform in all_platforms]
