from flask import Blueprint

bp = Blueprint('qa', __name__, url_prefix='/')

@bp.route('/', methods=['GET'])
def index():
    pass