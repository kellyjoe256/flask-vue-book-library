import re
from flask import request
from flask_restful import Resource, inputs, reqparse
from flask_jwt_extended import create_access_token, jwt_required, jwt_optional
from sqlalchemy.orm import subqueryload
from app.models import Book, Author, Category
from app.helpers import PaginationFormatter


def book_rules():
    str_regex = r'^[\w ]+$'
    printable_regex = r'''
^[a-z0-9!"#$%&\'()*+,-./:;<=>?@\\^_`{|}~\[\] \t\n\r\x0b\x0c]+$
'''.strip()

    parser = reqparse.RequestParser()
    parser.add_argument('isbn', required=True, trim=True,
                        help='ISBN is required', location='json')
    parser.add_argument('title', required=True,
                        type=inputs.regex(str_regex, re.IGNORECASE),
                        trim=True, help='Title is required', location='json')
    parser.add_argument('num_of_pages', required=True, type=inputs.positive,
                        help='Number of pages is required and must be a positive number', location='json')
    parser.add_argument('publisher', required=True,
                        type=inputs.regex(str_regex, re.IGNORECASE),
                        trim=True, help='Publisher is required',
                        location='json')
    parser.add_argument('publication_date', required=True, type=inputs.date,
                        help='Publication date is required and must be a valid date', location='json')
    parser.add_argument('about', required=True,
                        type=inputs.regex(printable_regex, re.IGNORECASE),
                        trim=True, help='About is required', location='json')
    parser.add_argument('authors', required=True, type=int, action='append',
                        help='Author is required', location='json')
    parser.add_argument('categories', required=True, type=int, action='append',
                        help='Category is required', location='json')
    return parser


def append_authors_to_book(book, authors):
    if not authors:
        return

    if book.id:
        book.authors = []
        book.save()

    for author_id in authors:
        author = Author.find(author_id)
        if author:
            book.authors.append(author)


def append_categories_to_book(book, categories):
    if not categories:
        return

    if book.id:
        book.categories = []
        book.save()

    for category_id in categories:
        category = Category.find(category_id)
        if category:
            book.categories.append(category)


class BookListAPI(Resource):

    def __init__(self):
        self.parser = book_rules()
        super(BookListAPI, self).__init__()

    def get(self):
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)

        sort_order = (Book.publication_date.desc(), Book.title,)
        pagination = Book.query.order_by(*sort_order). \
            paginate(page=page, per_page=limit, error_out=False)
        books = [book.json() for book in pagination.items]

        return PaginationFormatter(pagination, books).data

    @jwt_required
    def post(self):
        data = self.parser.parse_args()
        if Book.query.filter(Book.isbn == data.get('isbn')).first():
            return dict(message='ISBN already exists'), 409

        authors = data.pop('authors', [])
        categories = data.pop('categories', [])

        book = Book(**data)
        append_authors_to_book(book, authors)
        append_categories_to_book(book, categories)
        book.save()

        return book.json(), 201


class BookAPI(Resource):

    def __init__(self):
        self.parser = book_rules()
        super(BookAPI, self).__init__()

    def get(self, id):
        load_options = (
            subqueryload(Book.authors),
            subqueryload(Book.categories),
        )
        book = Book.find_or_fail(id, load_options=load_options)
        data = book.json()
        data['authors'] = [book.json() for book in book.authors]
        data['categories'] = [categories.json()
                              for categories in book.categories]

        return data

    @jwt_required
    def put(self, id):
        book = Book.find_or_fail(id)

        data = self.parser.parse_args()
        authors = data.pop('authors', [])
        categories = data.pop('categories', [])

        for key, value in data.items():
            if key == 'isbn' and self.check_for_isbn(id, value):
                return dict(message='ISBN already exists'), 409
            setattr(book, key, value)

        append_authors_to_book(book, authors)
        append_categories_to_book(book, categories)
        book.save()

        return book.json()

    @jwt_required
    def delete(self, id):
        book = Book.find_or_fail(id)
        book.delete()

        return None, 204

    def check_for_isbn(self, id, isbn):
        return Book.query.filter(Book.id != id, Book.isbn == isbn).first()
