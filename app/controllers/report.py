from sqlalchemy.exc import SQLAlchemyError

from ..repositories.managers import ReportManager
from .base import BaseController


class ReportController(BaseController):
    manager = ReportManager

    @classmethod
    def get_report(cls):
        report = dict()
        try:
            report['top3-clients'] = cls.manager.get_top3_clients()
            report['most-profitable-month'] = cls.manager.get_most_profitable_month()
            report['most-wanted-ingredient'] = cls.manager.get_most_wanted_ingredient()
            report['most-wanted-beverage'] = cls.manager.get_most_wanted_beverage()
            return report, None
        except (SQLAlchemyError, RuntimeError) as ex:
            return None, str(ex)
