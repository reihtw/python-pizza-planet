import logging

from flask_seeder import Seeder, Faker
from flask_seeder.generator import Sequence, Integer

from app.plugins import db
from app.repositories.models import Beverage, Ingredient, Order, OrderBeverages, OrderDetail, Size

from seeds.generators import Datetime, Name, DNI, Phone, Address


ORDERS_AMOUNT = 250
CLIENTS_AMOUNT = 15

BEVERAGES = [
    {'name': 'Coke', 'price': 2},
    {'name': 'Wine Bottle', 'price': 15},
    {'name': 'Water', 'price': 0.5},
    {'name': 'Sprite', 'price': 2},
    {'name': 'Grape Juice', 'price': 2},
]

SIZES = [
    {'name': 'Kids', 'price': 2},
    {'name': 'Small', 'price': 4},
    {'name': 'Regular', 'price': 6},
    {'name': 'Large', 'price': 9},
    {'name': 'Extra Large', 'price': 13},
]

INGREDIENTS = [
    {'name': 'Pepperoni', 'price': 3},
    {'name': 'Cheese', 'price': 2},
    {'name': 'Extra Cheese', 'price': 3},
    {'name': 'Chicken', 'price': 2},
    {'name': 'Bacon', 'price': 2},
    {'name': 'Tuna', 'price': 4},
    {'name': 'Ham', 'price': 2},
    {'name': 'Sausage', 'price': 2},
    {'name': 'Onion', 'price': 1},
    {'name': 'Fresh garlic', 'price': 1},
    {'name': 'Tomato', 'price': 2},
    {'name': 'Fresh basil', 'price': 1},
    {'name': 'Mushroom', 'price': 2},
]


class DBSeeder(Seeder):

    def create_order_items(self, model: db.Model, data: list):
        total_items = len(data)

        faker = Faker(
            cls=model,
            init={
                '_id': Sequence(end=total_items),
                'name': '',
                'price': 0
            }
        )

        items = faker.create(total_items)
        for item in items:
            item.name = data[item._id - 1]['name']
            item.price = data[item._id - 1]['price']

        return items

    def create_orders(self):
        faker_order = Faker(
            cls=Order,
            init={
                '_id': Sequence(end=ORDERS_AMOUNT),
                'client_name': Name(),
                'client_dni': DNI(),
                'client_address': Address(),
                'client_phone': Phone(),
                'date': Datetime(min_year=2021),
                'total_price': 0,
                'size_id': Integer(end=len(SIZES))
            }
        )

        faker_order_details = Faker(
            cls=OrderDetail,
            init={
                '_id': Sequence(end=ORDERS_AMOUNT),
                'ingredient_price': 0,
                'order_id': Integer(end=ORDERS_AMOUNT),
                'ingredient_id': Integer(end=len(INGREDIENTS))
            }
        )

        faker_order_beverages = Faker(
            cls=OrderBeverages,
            init={
                '_id': Sequence(end=ORDERS_AMOUNT),
                'beverage_price': 0,
                'order_id': Integer(end=ORDERS_AMOUNT),
                'beverage_id': Integer(end=len(BEVERAGES))
            }
        )

        order_details = faker_order_details.create(ORDERS_AMOUNT)
        order_beverages = faker_order_beverages.create(ORDERS_AMOUNT)
        for order_detail, order_beverage in zip(order_details, order_beverages):
            order_detail.ingredient_price = INGREDIENTS[order_detail.ingredient_id - 1]['price']
            order_beverage.beverage_price = BEVERAGES[order_beverage.beverage_id - 1]['price']

        clients = dict()
        orders = faker_order.create(ORDERS_AMOUNT)
        for order in orders:
            total_price_ingredients = sum([order_detail.ingredient_price for order_detail in order_details if order._id == order_detail.order_id])
            total_price_beverages = sum([order_beverage.beverage_price for order_beverage in order_beverages if order._id == order_beverage.order_id])
            order.total_price = SIZES[order.size_id - 1]['price'] + total_price_ingredients + total_price_beverages

            if order.client_dni not in clients:
                clients[order.client_dni] = {
                    'name': order.client_name,
                    'address': order.client_address,
                    'phone': order.client_phone
                }
                continue

            client = clients[order.client_dni]
            order.client_name = client['name']
            order.client_address = client['address']
            order.client_phone = client['phone']

        return orders, order_details, order_beverages

    def run(self):
        sizes = self.create_order_items(Size, SIZES)
        ingredients = self.create_order_items(Ingredient, INGREDIENTS)
        beverages = self.create_order_items(Beverage, BEVERAGES)
        orders, order_details, order_beverages = self.create_orders()

        logging.info('[O] Creating Sizes...')
        self.db.session.add_all(sizes)

        logging.info('[O] Creating Ingredients...')
        self.db.session.add_all(ingredients)

        logging.info('[O] Creating Beverages...')
        self.db.session.add_all(beverages)

        logging.info('[O] Creating Orders...')
        self.db.session.add_all(orders)

        logging.info('[O] Creating Order Details...')
        self.db.session.add_all(order_details)

        logging.info('[O] Creating Order Beverages...')
        self.db.session.add_all(order_beverages)

        self.db.session.commit()
        logging.info('[*] Success! All the data was created')
