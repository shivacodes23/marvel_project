from flask import Blueprint

bp = Blueprint('authorize',__name__, url_prefix='auth')

from . import routes, models