from ast import literal_eval
from urllib.parse import unquote
from six import text_type
from flask_restful import reqparse
from flask.json import JSONEncoder


class ArgumentsParser(object):

    @staticmethod
    def parse():
        parser = reqparse.RequestParser()
        parser.add_argument(
            'filter', dest='filter',
            type=str, help='Filter for searching items'
        )
        parser.add_argument(
            'schema', dest='schema',
            type=str, help='Schema for dumping the JSON'
        )
        parser.add_argument(
            'limit', dest='limit', default=80,
            type=int, help='Limit results'
        )
        parser.add_argument(
            'offset', dest='offset', default=0,
            type=int, help='Offset of results'
        )
        args = parser.parse_args()
        limit = args.limit
        offset = args.offset
        search_params = []
        if args.filter:
            try:
                search_params = literal_eval(unquote(args.filter))
            except (ValueError, SyntaxError) as e:
                raise
        return search_params, limit, offset


class LazyInt(object):
    def __init__(self, func, *args, **kwargs):
        self._func = func
        self._args = args
        self._kwargs = kwargs

    def __getattr__(self, attr):
        if attr == "__setstate__":
            raise AttributeError(attr)
        integer = int(self)
        if hasattr(integer, attr):
            return getattr(integer, attr)
        raise AttributeError(attr)

    def __repr__(self):
        return "l'{0}'".format(text_type(self))

    def __str__(self):
        return text_type(self._func(*self._args, **self._kwargs))

    def __add__(self, other):
        return int(self) + other

    def __radd__(self, other):
        return other + int(self)

    def __mul__(self, other):
        return int(self) * other

    def __rmul__(self, other):
        return other * int(self)

    def __lt__(self, other):
        return int(self) < other

    def __le__(self, other):
        return int(self) <= other

    def __eq__(self, other):
        return int(self) == other

    def __ne__(self, other):
        return int(self) != other

    def __gt__(self, other):
        return int(self) > other

    def __ge__(self, other):
        return int(self) >= other

    def __hash__(self):
        return hash(text_type(self))

    def __mod__(self, other):
        return int(self) % other

    def __rmod__(self, other):
        return other + int(self)

    def __int__(self):
        return int(str(self))


class CustomJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, LazyInt):
            return int(o)
        return super(CustomJSONEncoder, self).default(o)


