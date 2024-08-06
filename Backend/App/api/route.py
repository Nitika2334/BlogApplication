from flask import Blueprint
from flask_restful import Api
from App.api.wrapper.apis import LoginResource, LogoutResource, RegisterResource,PostResource

route = Blueprint('route', __name__)
api_v1 = Api(route)

api_v1.add_resource(RegisterResource, '/register')

api_v1.add_resource(LoginResource, '/login')

api_v1.add_resource(LogoutResource, '/logout')

api_v1.add_resource(PostResource, '/posts', '/posts/<uuid:post_id>')