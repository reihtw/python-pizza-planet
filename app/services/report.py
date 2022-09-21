from app.common.http_methods import GET
from flask import Blueprint

from app.controllers import ReportController
from ._base_service import BaseService

report = Blueprint('report', __name__)


@report.route('/', methods=GET)
@BaseService
def get_report():
    return ReportController.get_report()
