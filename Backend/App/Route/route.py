from flask import Blueprint
from flask_restful import Api
from ..wrapper.apis import LoginResource, LogoutResource

route = Blueprint('route', __name__)
api_v1 = Api(route)

api_v1.add_resource(LoginResource, '/login')

api_v1.add_resource(LogoutResource, '/logout')
