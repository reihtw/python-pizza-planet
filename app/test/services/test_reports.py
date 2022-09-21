import pytest


def test_generate_report_service(client, report_uri, create_orders):
    response = client.get(report_uri)
    report = response.json

    pytest.assume(response.status.startswith('200'))
    pytest.assume(report['most-profitable-month'])
    pytest.assume(report['most-wanted-beverage'])
    pytest.assume(report['most-wanted-ingredient'])
    pytest.assume(report['top3-clients'])
