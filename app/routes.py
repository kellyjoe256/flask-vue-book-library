from app.resources.auth import LoginAPI, LogoutAPI, MeAPI
from app.resources.author import AuthorListAPI, AuthorAPI
from app.resources.category import CategoryListAPI, CategoryAPI
from app.resources.book import BookListAPI, BookAPI
from app.resources.user import UserListAPI, UserAPI


def create_routes(api):
    # auth
    route = '/api/auth'
    api.add_resource(MeAPI, '{}/me'.format(route))
    api.add_resource(LoginAPI, '{}/login'.format(route))
    api.add_resource(LogoutAPI, '{}/logout'.format(route))

    # categories
    route = '/api/categories'
    api.add_resource(CategoryListAPI, route, endpoint='categories')
    api.add_resource(CategoryAPI, '{}/<int:id>'.format(route))

    # authors
    route = '/api/authors'
    api.add_resource(AuthorListAPI, route, endpoint='authors')
    api.add_resource(AuthorAPI, '{}/<int:id>'.format(route))

    # books
    route = '/api/books'
    api.add_resource(BookListAPI, route, endpoint='books')
    api.add_resource(BookAPI, '{}/<int:id>'.format(route))

    # users
    route = '/api/users'
    api.add_resource(UserListAPI, route, endpoint='users')
    api.add_resource(UserAPI, '{}/<int:id>'.format(route))
