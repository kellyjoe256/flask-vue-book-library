from flask import jsonify, make_response
from flask_restful import Resource, reqparse
from flask_jwt_extended import (jwt_required, create_access_token,
                                set_access_cookies, get_jwt_identity,
                                unset_jwt_cookies)
from app.models import User
from app.helpers import convert_to_dict


class LoginResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True, trim=True,
                        help='Username is required')
    parser.add_argument('password', required=True,
                        help='Password is required')

    def post(self):
        data = type(self).parser.parse_args()
        username = data.get('username', '')

        user = User.query.filter(User.username == username).first()
        if not (user and user.verify_password(data.get('password'))):
            return {'message': 'Invalid credentials'}, 401

        access_token = create_access_token(identity=user)
        response = make_response(jsonify(user.json()))
        response.headers['Content-Type'] = 'application/json'
        set_access_cookies(response, access_token)

        return response


class LogoutResource(Resource):

    @jwt_required
    def post(self):
        response = make_response(convert_to_dict(get_jwt_identity()))

        unset_jwt_cookies(response)

        return response


class MeResource(Resource):

    @jwt_required
    def get(self):
        return convert_to_dict(get_jwt_identity())
