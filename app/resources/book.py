from flask import request
from flask_restful import Resource, inputs, reqparse
from flask_jwt_extended import create_access_token, jwt_required, jwt_optional
from sqlalchemy.orm import subqueryload
from app.models import Book
from app.helpers import PaginationFormatter


def book_rules():
    parser = reqparse.RequestParser()
    parser.add_argument('isbn', required=True, trim=True,
                        help='ISBN is required', location='json')
    parser.add_argument('title', required=True, trim=True,
                        help='Title is required', location='json')
    parser.add_argument('num_of_pages', required=True, type=inputs.positive,
                        help='Number of pages is required and must be a positive number', location='json')
    parser.add_argument('publisher', required=True, trim=True,
                        help='Publisher is required', location='json')
    parser.add_argument('publication_date', required=True, type=inputs.date,
                        help='Publication date is required and must be a valid date', location='json')
    parser.add_argument('about', required=True, trim=True,
                        help='About is required', location='json')
    return parser


class BookListAPI(Resource):

    def __init__(self):
        self.parser = book_rules()
        super(BookListAPI, self).__init__()

    @jwt_optional
    def get(self):
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)

        pagination = Book.query.paginate(page=page, per_page=limit,
                                         error_out=False)
        books = [book.json() for book in pagination.items]

        return PaginationFormatter(pagination, books).data

    @jwt_required
    def post(self):
        data = self.parser.parse_args()
        if Book.query.filter(Book.isbn == data.get('isbn')).first():
            return dict(message='ISBN already exists'), 409

        book = Book(**data)
        book.save()

        return book.json(), 201


class BookAPI(Resource):

    def __init__(self):
        self.parser = book_rules()
        super(BookAPI, self).__init__()

    @jwt_optional
    def get(self, id):
        load_options = subqueryload("*")
        book = Book.find_or_fail(id, load_options=load_options)
        data = book.json()
        data['authors'] = book.authors
        data['categories'] = book.categories

        return data

    @jwt_required
    def put(self, id):
        book = Book.find_or_fail(id)

        data = self.parser.parse_args()
        for key, value in data.items():
            setattr(book, key, value)
        book.save()

        return book.json()

    @jwt_required
    def delete(self, id):
        book = Book.find_or_fail(id)
        book.delete()

        return None, 204
