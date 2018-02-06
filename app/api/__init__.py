#from app.api import routes, errors, status
from flask import Blueprint
from flask_restful import Api, Resource

api_bp = Blueprint('api', __name__)
api_api = Api(api_bp)

from app.api import routes, status

