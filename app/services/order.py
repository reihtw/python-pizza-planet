from app.common.http_methods import GET, POST
from flask import Blueprint, request

from ._base_service import BaseService
from ..controllers import OrderController

order = Blueprint('order', __name__)


@order.route('/', methods=POST)
@BaseService
def create_order():
    return OrderController.create(request.json)


@order.route('/id/<_id>', methods=GET)
@BaseService
def get_order_by_id(_id: int):
    return OrderController.get_by_id(_id)


@order.route('/', methods=GET)
@BaseService
def get_orders():
    return OrderController.get_all()
