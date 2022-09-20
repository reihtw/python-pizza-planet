from flask import jsonify
from typing import Any, Optional
from http import HTTPStatus


class BaseService:

    def __init__(self, function: callable):
        self.function = function
        self.__name__ = function.__name__

    def __call__(self, *args, **kwargs):
        item, error = self.function(*args, **kwargs)
        response, status_code = self.__get_response(item, error)
        return jsonify(response), status_code

    def __get_response(self, item: Any, error: Optional[str]):
        return self.___get_response_body(item, error), self.__get_status_code(item, error)

    def ___get_response_body(self, item: Any, error: Optional[str]):
        return item if not error else {'error': error}

    def __get_status_code(self, item: Any, error: Optional[str]):
        status_code = HTTPStatus.OK
        if error:
            status_code = HTTPStatus.BAD_REQUEST
        elif not item:
            status_code = HTTPStatus.NOT_FOUND
        elif 'create' in self.__name__:
            status_code = HTTPStatus.CREATED

        return status_code
