from flask import Blueprint

verifications_bp = Blueprint('verifications', __name__)

from . import routes, controller, forms