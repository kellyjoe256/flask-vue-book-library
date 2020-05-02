from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required, jwt_optional
from app.models import Category
from app.helpers import PaginationFormatter


def category_rules():
    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True, trim=True,
                        help='Name is required', location='json')
    return parser


class CategoryListAPI(Resource):

    def __init__(self):
        self.parser = category_rules()
        super(CategoryListAPI, self).__init__()

    @jwt_optional
    def get(self):
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)

        pagination = Category.query.paginate(page=page, per_page=limit,
                                             error_out=False)
        Categorys = [Category.json() for Category in pagination.items]

        return PaginationFormatter(pagination, Categorys).data

    @jwt_required
    def post(self):
        data = self.parser.parse_args()
        if Category.query.filter(Category.name == data.get('name')).first():
            return dict(message='Category already exists'), 409

        category = Category(**data)
        category.save()

        return category.json(), 201


class CategoryAPI(Resource):

    def __init__(self):
        self.parser = category_rules()
        super(CategoryAPI, self).__init__()

    @jwt_optional
    def get(self, id):
        category = Category.find_or_fail(id)

        return category.json()

    @jwt_required
    def put(self, id):
        category = Category.find_or_fail(id)

        data = self.parser.parse_args()
        for key, value in data.items():
            setattr(category, key, value)
        category.save()

        return category.json()

    @jwt_required
    def delete(self, id):
        category = Category.find_or_fail(id)
        category.delete()

        return None, 204
