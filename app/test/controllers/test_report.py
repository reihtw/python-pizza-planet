import pytest

from app.controllers import ReportController


def __get_item_quantities(orders):
    ingredient_quantities = dict()
    beverages_quantities = dict()
    for order in orders:
        for ingredient in order.pop('detail', []):
            _id = ingredient['ingredient']['_id']
            if _id not in ingredient_quantities:
                ingredient_quantities[_id] = 0
            ingredient_quantities[_id] += 1

        for beverage in order.pop('beverages', []):
            _id = beverage['beverage']['_id']
            if _id not in beverages_quantities:
                beverages_quantities[_id] = 0
            beverages_quantities[_id] += 1

    return ingredient_quantities, beverages_quantities


def __get_month_amount(orders):
    month_amount = dict()
    for order in orders:
        month = order['date'].rsplit('-', 1)[0]
        if month not in month_amount:
            month_amount[month] = 0
        month_amount[month] += order['total_price']
    return month_amount


def __get_clients_total_purchases_amount(orders):
    clients_purchases = dict()
    for order in orders:
        client_name = order['client_name']
        if client_name not in clients_purchases:
            clients_purchases[client_name] = 0
        clients_purchases[client_name] += order['total_price']
    return clients_purchases


def test_get_report(app, create_orders):
    orders = create_orders

    ingredient_quantities, beverage_quantities = __get_item_quantities(orders)
    print(ingredient_quantities, beverage_quantities)
    month_amount = __get_month_amount(orders)
    clients_purchases_amount = __get_clients_total_purchases_amount(orders)

    most_wanted_ingredient_id = sorted(zip(ingredient_quantities.values(), ingredient_quantities.keys()), reverse=True)[0][1]
    most_wanted_beverage_id = sorted(zip(beverage_quantities.values(), beverage_quantities.keys()), reverse=True)[0][1]

    created_report, error = ReportController.get_report()
    most_profitable_month = max(month_amount, key=month_amount.get)
    top3_clients = sorted(zip(clients_purchases_amount.values(), clients_purchases_amount.keys()), reverse=True)[:3]

    pytest.assume(error is None)
    pytest.assume(created_report['most-wanted-ingredient']['ingredient']['_id'] == most_wanted_ingredient_id)
    pytest.assume(created_report['most-wanted-beverage']['beverage']['_id'] == most_wanted_beverage_id)
    pytest.assume(created_report['most-profitable-month']['month'] == most_profitable_month)
    for index, client in enumerate(top3_clients):
        pytest.assume(created_report['top3-clients'][index]['client_name'] == client[1])
        pytest.assume(created_report['top3-clients'][index]['amount_spent'] == client[0])
