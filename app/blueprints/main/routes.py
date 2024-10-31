from flask import render_template, redirect, url_for, request, jsonify
from app.forms.login import LoginForm
from app.blueprints.main import bp
from app.models.product import Product
from app.forms.payment_form import PaymentForm
from app.extensions import paypal
import os

@bp.route('/')
def home():
    login_form = LoginForm()
    latest_products = Product.latest_products()
    return render_template('index.html', form=login_form, last_products=latest_products)

@bp.route('/product/<slug>')
def product(slug):
    product_item = Product.search_product_slug(slug)
    form = PaymentForm()
    form.amount.data = product_item.product_keys[0].key_info.price
    form.product_id.data = product_item.id
    return render_template('product.html', product=product_item, form=form)

@bp.route('/pay/<product_id>', methods=['POST'])
def pay(product_id):
    product_info = Product.get_product(product_id)
    amount = product_info.product_keys[0].key_info.price
    payment = paypal.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "transactions": [{
            "amount": {
                "total": "{:.2f}".format(amount),
                "currency": "USD"
        },
        "description": "Payment for your service from flask"
        }],
        "redirect_urls": {
            "return_url": f"{os.environ.get('DOMAIN')}/payment/success",
            "cancel_url": f"{os.environ.get('DOMAIN')}/payment/rejected"
        }

    })

    if payment.create():
        for link in payment.links:
            if link.method == 'REDIRECT':
                redirect_url = str(link.href)
                return redirect(redirect_url)
    else:
        return jsonify({'error': payment.error}), 400


@bp.route('/payment/success')
def payment_success():
    return redirect(url_for('main.home'))


@bp.route('/payment/rejected')
def payment_rejected():
    return redirect(url_for('products.index'))
