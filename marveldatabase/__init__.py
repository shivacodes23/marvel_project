from flask import Blueprint

bp = Blueprint('marvel', __name__, url_prefix=('/'))

from . import models, routes