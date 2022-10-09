from flask import Blueprint
from views.chronic_disease import metric  # noqa


app = Blueprint('chronic_disease', __name__, url_prefix="/chronic_disease")
