from app.main import bp

@bp.route('/')
def home():
    return 'this is the main blueprint'

@bp.route('/pedro')
def pedro():
    return 'this is another route'