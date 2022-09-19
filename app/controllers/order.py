from sqlalchemy.exc import SQLAlchemyError

from ..common.utils import check_required_keys
from ..repositories.managers import (BeverageManager, IngredientManager, OrderManager,
                                     SizeManager)
from .base import BaseController


class OrderController(BaseController):
    manager = OrderManager
    __required_info = ('client_name', 'client_dni', 'client_address', 'client_phone', 'size_id')

    @staticmethod
    def calculate_order_price(size_price: float, ingredients: list, beverages: list):
        def calculate_item_list_total_price(items):
            return sum(item.price for item in items)

        ingredients_total_price = calculate_item_list_total_price(ingredients)
        beverages_total_price = calculate_item_list_total_price(beverages)
        total_price = size_price + ingredients_total_price + beverages_total_price
        return round(total_price, 2)

    @classmethod
    def create(cls, order: dict):
        current_order = order.copy()
        if not check_required_keys(cls.__required_info, current_order):
            return 'Invalid order payload', None

        size_id = current_order.get('size_id')
        size = SizeManager.get_by_id(size_id)

        if not size:
            return 'Invalid size for Order', None

        ingredient_ids = current_order.pop('ingredients', [])
        beverages_ids = current_order.pop('beverages', [])
        try:
            ingredients = IngredientManager.get_by_id_list(ingredient_ids)
            beverages = BeverageManager.get_by_id_list(beverages_ids)
            price = cls.calculate_order_price(size.get('price'), ingredients, beverages)
            order_with_price = {**current_order, 'total_price': price}
            return cls.manager.create(order_with_price, ingredients, beverages), None
        except (SQLAlchemyError, RuntimeError) as ex:
            return None, str(ex)
