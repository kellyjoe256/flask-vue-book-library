import json
from flask import jsonify, make_response
from flask_restful import Resource, reqparse
from flask_jwt_extended import (jwt_required, create_access_token,
                                set_access_cookies, get_jwt_identity,
                                unset_jwt_cookies)
from app.models import User


class LoginAPI(Resource):
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('username', required=True, trim=True,
                        help='Username is required')
    parser.add_argument('password', required=True,
                        help='Password is required')

    def post(self):
        data = type(self).parser.parse_args()
        username = data.get('username', '')

        user = User.query.filter(User.username == username).first()
        if not (user and user.verify_password(data.get('password'))):
            return {'message': 'Username or Password incorrect'}, 401

        access_token = create_access_token(identity=user)
        response = make_response(jsonify(user.json()))
        response.headers['Content-Type'] = 'application/json'
        set_access_cookies(response, access_token)

        return response


class LogoutAPI(Resource):

    @jwt_required
    def post(self):
        response = make_response()
        unset_jwt_cookies(response)

        return response


class MeAPI(Resource):

    @jwt_required
    def get(self):
        return json.loads(get_jwt_identity())
