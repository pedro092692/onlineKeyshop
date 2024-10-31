from flask import render_template, redirect, url_for, request
from app.forms.admin.add_products import AddProduct
from app.forms.admin.update_product_form import UpdateProduct
from app.forms.admin.add_category_form import AddCategory as SimpleForm, AddCategory
from app.forms.admin.add_subcategory_form import SubcategoryForm
from app.forms.admin.add_new_key_form import AddKey
from app.models.category import Category
from app.models.sub_category import SubCategory
from app.models.platforms import Platform
from app.models.product import Product
from app.models.key import Key
from app.models.product_keys import ProductKeys
from app.extensions import generate_password_hash, turbo
from app.blueprints.admin import bp


@bp.route('/')
def index():
    return render_template('admin/index.html')

# products
@bp.route('/products', methods=['GET', 'POST'])
def products():
    all_products = Product.get_products()
    # search products
    if request.method == 'POST':
        product_query = request.form.get('product_search')
        if product_query != '':
            search_results = Product.search_product(product_query)
            if turbo.can_stream():
                return turbo.stream([
                    turbo.update(render_template('admin/includes/products/__table_content.html',
                                                 products=search_results), target='product-list')
                ])

    if turbo.can_stream():
        return turbo.stream([
            turbo.update(render_template('admin/includes/products/__table_content.html',
                                            products=all_products), target='product-list')
        ])

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
        img_url = form.image_url.data
        #key info
        product_key =  generate_password_hash(password=form.product_key_code.data, method='pbkdf2:sha256', salt_length=8)
        product_price = form.product_price.data

        # add new product
        new_product = Product.add_product(Product, product_name, platform_id, category_id, subcategory_id, img_url)
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
        img_url = form_product.image_url.data
        # update product
        Product.update_product(product, product_name,
                               platform_id,
                               category_id,
                               subcategory_id,
                               img_url
                               )
        return redirect(url_for('admin.products'))

    form_product.name.data = product.name
    form_product.product_category.data = product.category_id
    form_product.product_platform.data = product.platform_id
    form_product.product_subcategory.data = product.sub_category_id
    form_product.image_url.data = product.img_url

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
@bp.route('/categories', methods=['GET', 'POST'])
def categories():
    all_categories = Category.categories_paginate()
    # search category
    if request.method == 'POST':
        category_query = request.form.get('category_search')
        if category_query != '':
            search_results = Category.search_category(category_query)
            if turbo.can_stream():
                return turbo.stream([
                    turbo.update(render_template('admin/includes/categories/__table_content.html',
                                                 categories=search_results), target='category-list')
                ])
    return render_template('admin/categories/index.html', categories=all_categories)

@bp.route('/add-category', methods=['GET', 'POST'])
def add_category():
    form = SimpleForm()
    if form.validate_on_submit():
        category_name = form.name.data
        Category.add_category(Category, category_name)
        return redirect(url_for('admin.categories'))
    return render_template('admin/categories/add-category.html', form=form)

@bp.route('/category/<category_id>', methods=['GET', 'POST'])
def category_info(category_id):
    category = Category.get_category(category_id)
    form = AddCategory()
    if form.validate_on_submit():
        category_name = form.name.data
        Category.update_category(category, category_name)
        return redirect(url_for('admin.categories'))
    # fill form
    form.name.data = category.name
    form.submit.label.text = 'Update Category'

    return render_template('admin/categories/category.html', form=form, category=category)

@bp.route('/category/delete/<category_id>', methods=['POST'])
def delete_category(category_id):
    category = Category.get_category(category_id)
    Category.delete_category(category)
    return redirect(url_for('admin.categories'))

#subcategories
@bp.route('/subcategories', methods=['GET', 'POST'])
def subcategories():
    all_subcategories = SubCategory.subcategories_paginate()
    #search subcategory
    if request.method == 'POST':
        subcategory_query = request.form.get('subcategory_search')
        if subcategory_query != '':
            search_results = SubCategory.search_subcategory(subcategory_query)
            if turbo.can_stream():
                return turbo.stream([
                    turbo.update(render_template('admin/includes/subcategories/__table_content.html',
                                                 subcategories=search_results), target='subcategory-list')
                ])
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

@bp.route('/subcategory/<subcategory_id>', methods=['GET', 'POST'])
def subcategory_info(subcategory_id):
    subcategory = SubCategory.get_subcategory(subcategory_id)

    # form for products
    product_form = AddProduct()

    # fill form product_choices
    fill_form_product(product_form)

    product_form.product_category.data = subcategory.category_id
    product_form.product_subcategory.data = subcategory.id

    if product_form.submit.data and product_form.validate():
        product_name = product_form.product_name.data
        subcategory_id = product_form.product_subcategory.data
        category_id = product_form.product_category.data
        platform_id = product_form.product_platform.data
        product_key = generate_password_hash(product_form.product_key_code.data, method='pbkdf2:sha256', salt_length=8)
        product_price = product_form.product_price.data

        # add new product
        new_product = Product.add_product(Product, product_name, platform_id, category_id, subcategory_id)
        # add new key
        new_key = Key.add_key(Key, product_key, 0, product_price)
        # add new product key
        ProductKeys.add_new_product_key(ProductKeys, new_product.id, new_key.id)

        return redirect(url_for('admin.products'))


    form = SubcategoryForm()
    categories_ = Category.categories()
    form.category_id.choices = [(0, 'Select One')] + [(category.id, category.name) for category in categories_]
    if form.submit.data and form.validate():
        subcategory_name = form.name.data
        category_id = form.category_id.data
        #update subcategory
        SubCategory.update_subcategory(subcategory, category_id, subcategory_name)
        return redirect(url_for('admin.subcategories'))

    #fill form to update subcategory
    form.name.data = subcategory.name
    form.category_id.data = subcategory.category_id

    form.submit.label.text = 'Update Subcategory'

    return render_template('admin/subcategories/subcategory.html', subcategory=subcategory, form=form,
                           product_form=product_form)

@bp.route('/subcategory/delete/<subcategory_id>', methods=['POST'])
def delete_subcategory(subcategory_id):
    subcategory = SubCategory.get_subcategory(subcategory_id)
    SubCategory.delete_subcategory(subcategory)
    return redirect(url_for('admin.subcategories'))

#platforms
@bp.route('/platforms', methods=['GET', 'POST'])
def platforms():
    all_platforms = Platform.platforms_paginate()
    if request.method == 'POST':
        platform_query = request.form.get('platform_search')
        if platform_query != '':
            all_platforms = Platform.search_platform(platform_query)
            if turbo.can_stream():
                return turbo.stream([
                    turbo.update(render_template('admin/includes/platforms/__table_content.html',
                                                 platforms=all_platforms), target='platforms-list')
                ])

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

@bp.route('/platform/<platform_id>', methods=['GET', 'POST'])
def platform_info(platform_id):
    platform = Platform.get_platform(platform_id)
    form = SimpleForm()
    # config form
    form.name.label = 'Platform Name'
    form.submit.label.text = 'Update Platform'

    if form.validate_on_submit():
        platform_name = form.name.data
        Platform.update_platform(platform, platform_name)
        return redirect(url_for('admin.platforms'))

    form.name.data = platform.name

    return render_template('admin/platforms/platform.html', platform=platform, form=form)

@bp.route('/platform/delete/<platform_id>', methods=['POST'])
def delete_platform(platform_id):
    platform_obj = Platform.get_platform(platform_id)
    Platform.delete_platform(platform_obj)
    return redirect(url_for('admin.platforms'))

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


