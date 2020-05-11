from flask import request
from flask_restful import Resource, inputs, reqparse
from flask_jwt_extended import (create_access_token, jwt_required)
from app.models import User
from app.helpers import is_admin, PaginationFormatter


def user_rules():
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('username', required=True,
                        type=inputs.regex(r'^[a-zA-Z0-9_]+$'),
                        trim=True, help='Username is required', location='json')
    parser.add_argument('password', required=True,
                        type=inputs.regex(r'^[A-Za-z@!~#$%^&*()-+\d]{8,}$'),
                        trim=True, help='Password is required', location='json')
    parser.add_argument('is_admin', type=inputs.boolean, default=False,
                        location='json')
    return parser


class UserListAPI(Resource):

    decorators = [jwt_required, is_admin]

    def __init__(self):
        self.parser = user_rules()
        super(UserListAPI, self).__init__()

    def get(self):
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)

        pagination = User.query.paginate(page=page, per_page=limit,
                                         error_out=False)
        users = [user.json() for user in pagination.items]

        return PaginationFormatter(pagination, users).data

    def post(self):
        data = self.parser.parse_args()
        if User.query.filter(User.username == data.get('username')).first():
            return dict(message='Username already exists'), 409

        user = User(**data)
        user.save()

        return user.json(), 201


class UserAPI(Resource):

    decorators = [jwt_required, is_admin]

    def __init__(self):
        self.parser = user_rules()
        super(UserAPI, self).__init__()

    def get(self, id):
        user = User.find_or_fail(id)

        return user.json()

    def put(self, id):
        user = User.find_or_fail(id)

        self.parser.replace_argument('password',
                                     type=inputs.regex(
                                         r'^[A-Za-z@!~#$%^&*()-+\d]{8,}$'),
                                     help='Password is required', location='json')

        data = self.parser.parse_args()
        if not data.get('password'):
            data.pop('password', None)

        for key, value in data.items():
            if key == 'username' and self.check_for_username(id, value):
                return dict(message='Username already exists'), 409
            setattr(user, key, value)
        user.save()

        return user.json()

    def delete(self, id):
        user = User.find_or_fail(id)
        user.delete()

        return None, 204

    def check_for_username(self, id, username):
        return User.query.filter(User.id != id, User.username == username). \
            first()
