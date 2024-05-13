from flask import Blueprint

app = Blueprint('fujix', __name__, url_prefix="/fujix")

from views.fujix import index  # noqa
