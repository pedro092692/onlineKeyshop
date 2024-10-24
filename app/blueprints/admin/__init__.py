from flask import Blueprint, abort
from app.extensions import current_user

bp = Blueprint('admin', __name__)

@bp.before_request
def check_login():
    if not current_user.is_authenticated:
        return abort(403)

from app.blueprints.admin import routes