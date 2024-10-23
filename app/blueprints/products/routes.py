from flask import render_template
from app.blueprints.products import bp
from app.models.product import Product
from app.models.platforms import Platform
from app.models.category import Category
from app.models.sub_category import SubCategory

@bp.route('/')
def index():
    latest_products = Product.latest_products()
    latest_gift_cards = Product.get_latest_gift_cards()
    platforms = Platform.get_platforms()
    categories = Category.get_categories()
    subcategories = SubCategory.get_subcategories()
    return render_template('products/index.html', last_products=latest_products,
                           latest_gift_cards=latest_gift_cards,
                           platforms=platforms,
                           categories=categories,
                           subcategories=subcategories)


