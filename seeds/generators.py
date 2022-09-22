import random

from flask_seeder.generator import Generator
from datetime import datetime, timedelta


def read_resource(path):
    """ Read resource text file

    Reads resource text file and returns content as a list.

    Arguments:
        path: The resource path relative to the data root directory

    Returns:
        A list with the file contents.
    """
    lines = []
    with open(path) as source:
        lines = source.read().splitlines()

    return lines


class Datetime(Generator):

    def __init__(self, min_year=2021, max_year=datetime.now(), **kwargs):
        super(**kwargs).__init__()
        self._min_year = min_year
        self._max_year = max_year

    def generate(self):
        start = datetime(self._min_year, 1, 1, 00, 00, 00)
        end = self._max_year
        if not isinstance(self._max_year, datetime):
            years = self._max_year - self._min_year + 1
            end = start + timedelta(days=365 * years)
        return start + (end - start) * random.random()


class Name(Generator):
    """ Random Name generator """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._lines = None

    def generate(self):
        """ Generate a random name

        Returns:
            A random name in string format
        """
        if self._lines is None:
            self._lines = read_resource("seeds/data/names.txt")

        result = self.rnd.choice(self._lines)

        return result


class DNI(Generator):
    """ Random DNI generator """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._lines = None

    def generate(self):
        """ Generate a random DNI

        Returns:
            A random DNI in string format
        """
        if self._lines is None:
            self._lines = read_resource("seeds/data/dnis.txt")

        result = self.rnd.choice(self._lines)

        return result


class Address(Generator):
    """ Random Address generator """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._lines = None

    def generate(self):
        """ Generate a random DNI

        Returns:
            A random Address in string format
        """
        if self._lines is None:
            self._lines = read_resource("seeds/data/addresses.txt")

        result = self.rnd.choice(self._lines)

        return result


class Phone(Generator):
    """ Random Phone generator """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._lines = None

    def generate(self):
        """ Generate a random Phone

        Returns:
            A random Phones in string format
        """
        if self._lines is None:
            self._lines = read_resource("seeds/data/phones.txt")

        result = self.rnd.choice(self._lines)

        return result
