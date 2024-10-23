from flask import Blueprint

bp = Blueprint('products', __name__)

from app.blueprints.products import routes