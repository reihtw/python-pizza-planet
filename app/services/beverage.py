from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, request

from ._base_service import BaseService
from ..controllers import BeverageController

beverage = Blueprint('beverage', __name__)


@beverage.route('/', methods=POST)
@BaseService
def create_beverage():
    return BeverageController.create(request.json)


@beverage.route('/', methods=PUT)
@BaseService
def update_beverage():
    return BeverageController.update(request.json)


@beverage.route('/id/<_id>', methods=GET)
@BaseService
def get_beverage_by_id(_id: int):
    return BeverageController.get_by_id(_id)


@beverage.route('/', methods=GET)
@BaseService
def get_beverages():
    return BeverageController.get_all()
