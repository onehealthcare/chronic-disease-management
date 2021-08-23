from flask import Blueprint

app = Blueprint('chronic_condition', __name__, url_prefix="/chronic_condition")

from views.chronic_condition import index  # noqa
from views.chronic_condition import metric # noqa
from views.chronic_condition import measure # noqa
