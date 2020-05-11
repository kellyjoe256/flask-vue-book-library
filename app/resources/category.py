import re
from flask import request
from flask_restful import Resource, inputs, reqparse
from flask_jwt_extended import create_access_token, jwt_required, jwt_optional
from app.models import Category
from app.helpers import PaginationFormatter


def category_rules():
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('name', required=True,
                        type=inputs.regex(r'^[\w ]+$', re.IGNORECASE),
                        trim=True, help='Name is required', location='json')
    return parser


class CategoryListAPI(Resource):

    def __init__(self):
        self.parser = category_rules()
        super(CategoryListAPI, self).__init__()

    def get(self):
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        all = request.args.get('all', False, type=bool)

        if all:
            return [category.json() for category in self.all()]

        pagination = self.paginated(page, limit)
        categories = [Category.json() for Category in pagination.items]

        return PaginationFormatter(pagination, categories).data

    @jwt_required
    def post(self):
        data = self.parser.parse_args()
        if Category.query.filter(Category.name == data.get('name')).first():
            return dict(message='Category already exists'), 409

        category = Category(**data)
        category.save()

        return category.json(), 201

    def all(self):
        return Category.query.order_by(Category.name).all()

    def paginated(self, page, per_page):
        return Category.query.order_by(Category.name). \
            paginate(page=page, per_page=per_page, error_out=False)


class CategoryAPI(Resource):

    def __init__(self):
        self.parser = category_rules()
        super(CategoryAPI, self).__init__()

    def get(self, id):
        category = Category.find_or_fail(id)

        return category.json()

    @jwt_required
    def put(self, id):
        category = Category.find_or_fail(id)

        data = self.parser.parse_args()
        for key, value in data.items():
            if key == 'name' and self.check_for_name(id, value):
                return dict(message='Category already exists'), 409
            setattr(category, key, value)
        category.save()

        return category.json()

    @jwt_required
    def delete(self, id):
        category = Category.find_or_fail(id)
        category.delete()

        return None, 204

    def check_for_name(self, id, name):
        return Category.query. \
            filter(Category.id != id, Category.name == name). \
            first()
