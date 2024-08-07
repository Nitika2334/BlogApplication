from flask import Blueprint
from flask_restful import Api
from App.api.wrapper.apis import LoginResource, LogoutResource, HomePageResource,RegisterResource, CommentResource,PostResource

route = Blueprint('route', __name__)
api_v1 = Api(route)

api_v1.add_resource(RegisterResource, '/register')

api_v1.add_resource(LoginResource, '/login')

api_v1.add_resource(LogoutResource, '/logout')

api_v1.add_resource(HomePageResource, '/home')

api_v1.add_resource(PostResource, '/post', '/post/<uuid:post_id>')

api_v1.add_resource(CommentResource, '/posts/<uuid:post_id>/comments', '/comments/<uuid:comment_id>')
