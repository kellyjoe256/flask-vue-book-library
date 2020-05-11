import re
from flask import request
from flask_restful import Resource, inputs, reqparse
from flask_jwt_extended import create_access_token, jwt_required, jwt_optional
from sqlalchemy.orm import subqueryload
from app.models import Author
from app.helpers import PaginationFormatter


def author_rules():
    str_regex = r'^[\w ]+$'
    printable_regex = r'''
^[a-z0-9!"#$%&\'()*+,-./:;<=>?@\\^_`{|}~\[\] \t\n\r\x0b\x0c]+$
'''.strip()

    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('last_name', required=True,
                        type=inputs.regex(str_regex, re.IGNORECASE),
                        trim=True, help='Last name is required',
                        location='json')
    parser.add_argument('first_name', required=True,
                        type=inputs.regex(str_regex, re.IGNORECASE),
                        trim=True, help='First name is required',
                        location='json')
    parser.add_argument('gender', required=True, trim=True,
                        help='Gender is required', choices=('M', 'F',),
                        location='json')
    parser.add_argument('about', required=True,
                        type=inputs.regex(printable_regex, re.IGNORECASE),
                        trim=True, help='About is required', location='json')
    return parser


class AuthorListAPI(Resource):

    def __init__(self):
        self.parser = author_rules()
        super(AuthorListAPI, self).__init__()

    def get(self):
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        all = request.args.get('all', False, type=bool)

        if all:
            return [author.json() for author in self.all()]

        pagination = self.paginated(page, limit)
        authors = [author.json() for author in pagination.items]

        return PaginationFormatter(pagination, authors).data

    @jwt_required
    def post(self):
        data = self.parser.parse_args()
        author = Author(**data)
        author.save()

        return author.json(), 201

    def all(self):
        return Author.query.order_by(Author.first_name, Author.last_name).all()

    def paginated(self, page, per_page):
        return Author.query.order_by(Author.first_name, Author.last_name). \
            paginate(page=page, per_page=per_page, error_out=False)


class AuthorAPI(Resource):

    def __init__(self):
        self.parser = author_rules()
        super(AuthorAPI, self).__init__()

    def get(self, id):
        load_options = subqueryload(Author.books)
        author = Author.find_or_fail(id, load_options=load_options)
        data = author.json()
        data['books'] = [book.json() for book in author.books]

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
