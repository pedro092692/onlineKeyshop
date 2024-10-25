from flask import Blueprint, abort
from app.extensions import current_user, login_required

bp = Blueprint('admin', __name__)

@bp.before_request
@login_required
def check_admin():
    if current_user.role != 'admin':
        return abort(403)


from app.blueprints.admin import routes