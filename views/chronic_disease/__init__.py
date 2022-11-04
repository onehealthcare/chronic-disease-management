from flask import Blueprint

app = Blueprint('chronic_disease', __name__, url_prefix="/chronic_disease")

from views.chronic_disease import index, measure, metric  # noqa
