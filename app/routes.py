from app.resources.auth import (LoginResource, LogoutResource, MeResource)


def create_routes(api):
    # auth
    base_route = '/api/auth'
    api.add_resource(MeResource, '{}/me'.format(base_route))
    api.add_resource(LoginResource, '{}/login'.format(base_route))
    api.add_resource(LogoutResource, '{}/logout'.format(base_route))
