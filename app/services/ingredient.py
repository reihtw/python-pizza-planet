from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, request

from ._base_service import BaseService
from ..controllers import IngredientController

ingredient = Blueprint('ingredient', __name__)


@ingredient.route('/', methods=POST)
@BaseService
def create_ingredient():
    return IngredientController.create(request.json)


@ingredient.route('/', methods=PUT)
@BaseService
def update_ingredient():
    return IngredientController.update(request.json)


@ingredient.route('/id/<_id>', methods=GET)
@BaseService
def get_ingredient_by_id(_id: int):
    return IngredientController.get_by_id(_id)


@ingredient.route('/', methods=GET)
@BaseService
def get_ingredients():
    return IngredientController.get_all()
