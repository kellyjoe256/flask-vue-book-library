from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required, jwt_optional
from sqlalchemy.orm import subqueryload
from app.models import Author
from app.helpers import PaginationFormatter


def author_rules():
    parser = reqparse.RequestParser()
    parser.add_argument('last_name', required=True, trim=True,
                        help='Last name is required', location='json')
    parser.add_argument('first_name', required=True, trim=True,
                        help='First name is required', location='json')
    parser.add_argument('gender', required=True, trim=True,
                        help='Gender is required', choices=('M', 'F',),
                        location='json')
    parser.add_argument('about', required=True, trim=True,
                        help='About is required', location='json')
    return parser


class AuthorListAPI(Resource):

    def __init__(self):
        self.parser = author_rules()
        super(AuthorListAPI, self).__init__()

    @jwt_optional
    def get(self):
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)

        pagination = Author.query.paginate(page=page, per_page=limit,
                                           error_out=False)
        authors = [author.json() for author in pagination.items]

        return PaginationFormatter(pagination, authors).data

    @jwt_required
    def post(self):
        data = self.parser.parse_args()
        author = Author(**data)
        author.save()

        return author.json(), 201


class AuthorAPI(Resource):

    def __init__(self):
        self.parser = author_rules()
        super(AuthorAPI, self).__init__()

    @jwt_optional
    def get(self, id):
        load_options = subqueryload(Author.books)
        author = Author.find_or_fail(id, load_options=load_options)
        data = author.json()
        data['books'] = author.books

        return data

    @jwt_required
    def put(self, id):
        author = Author.find_or_fail(id)

        data = self.parser.parse_args()
        for key, value in data.items():
            setattr(author, key, value)
        author.save()

        return author.json()

    @jwt_required
    def delete(self, id):
        author = Author.find_or_fail(id)
        author.delete()

        return None, 204
