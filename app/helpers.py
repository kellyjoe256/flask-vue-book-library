import json
import query_string
from functools import wraps
from flask import abort, jsonify, request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity


def convert_to_dict(data):
    return json.loads(data.decode('utf-8'))


def abort_with_json(status_code, data=None):
    if data is None:
        data = {}
    response = jsonify(data)
    response.status_code = status_code
    abort(response)


def is_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        current_user = json.loads(get_jwt_identity())
        if not current_user.get('is_admin'):
            return abort_with_json(401, {'message': 'Must be an admin'})
        return func(*args, **kwargs)
    return wrapper


class PaginationFormatter(object):

    def __init__(self, pagination, data):
        self.pagination = pagination
        self.pagination_data = data
        self.base_url = request.base_url
        self.query_string = query_string.parse(request.url)

    @property
    def qs(self):
        return '&'.join((
            '{}={}'.format(k, v)
            for k, v in self.query_string.items()
        ))

    @qs.setter
    def qs(self, value):
        qs = self.query_string

        k, v = value
        qs[k] = v

        self.query_string = qs

    @property
    def data(self):
        return self.formatted_data()

    @data.setter
    def data(self, data):
        raise AttributeError('Cannot set data attribute')

    def first_link(self):
        self.qs = 'page', 1

        return '{}?{}'.format(self.base_url, self.qs)

    def last_link(self):
        self.qs = 'page', self.pagination.pages

        return '{}?{}'.format(self.base_url, self.qs)

    def next_link(self):
        next_page = self.pagination.next_num
        link = None
        if next_page:
            self.qs = 'page', next_page
            link = '{}?{}'.format(self.base_url, self.qs)

        return link

    def previous_link(self):
        previous_page = self.pagination.prev_num
        link = None
        if previous_page:
            self.qs = 'page', previous_page
            link = '{}?{}'.format(self.base_url, self.qs)

        return link

    def links(self):
        return dict(
            first=self.first_link(),
            last=self.last_link(),
            next=self.next_link(),
            previous=self.previous_link(),
        )

    def metadata(self):
        return dict(
            current_page=self.pagination.page,
            last_page=self.pagination.pages,
            per_page=self.pagination.per_page,
            total=self.pagination.total,
        )

    def formatted_data(self):
        return dict(
            data=self.pagination_data,
            meta=self.metadata(),
            links=self.links(),
        )
