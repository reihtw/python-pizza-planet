import pytest


def test_generate_report_service(client, report_uri, create_orders):
    response = client.get(report_uri)
    report = response.json

    pytest.assume(response.status.startswith('200'))
    pytest.assume(report['most_profitable_month'])
    pytest.assume(report['most_wanted_beverage'])
    pytest.assume(report['most_wanted_ingredient'])
    pytest.assume(report['top3_clients'])
