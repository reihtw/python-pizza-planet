import pytest
import logging

from ..utils.functions import (shuffle_list, get_random_sequence,
                               get_random_string)


def client_data_mock() -> dict:
    return {
        'client_address': get_random_string(),
        'client_dni': get_random_sequence(),
        'client_name': get_random_string(),
        'client_phone': get_random_sequence()
    }


@pytest.fixture
def order_uri():
    return '/order/'


@pytest.fixture
def client_data():
    return client_data_mock()


@pytest.fixture
def order(create_ingredients, create_beverages, create_sizes, client_data) -> dict:
    ingredients = [ingredient.get('_id') for ingredient in create_ingredients]
    beverages = [beverage.get('_id') for beverage in create_beverages]
    size_id = create_sizes[0].get('_id')
    return {
        **client_data_mock(),
        'ingredients': ingredients,
        'beverages': beverages,
        'size_id': size_id
    }


@pytest.fixture
def create_order(client, order_uri, order):
    return client.post(order_uri, json=order)


@pytest.fixture
def create_orders(client, order_uri, order) -> list:
    orders = []
    for _ in range(10):
        new_order = client.post(order_uri, json=order)
        orders.append(new_order.json)
    return orders
