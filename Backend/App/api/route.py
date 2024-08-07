from flask import Blueprint
from flask_restful import Api
from App.api.wrapper.apis import LoginResource, LogoutResource, HomePageResource, RegisterResource, CommentResource, PostResource
from App.api.logger import logger

route = Blueprint('route', __name__)
api_v1 = Api(route)

api_v1.add_resource(RegisterResource, '/register')
logger.info('RegisterResource endpoint added: /register')

api_v1.add_resource(LoginResource, '/login')
logger.info('LoginResource endpoint added: /login')

api_v1.add_resource(LogoutResource, '/logout')
logger.info('LogoutResource endpoint added: /logout')

api_v1.add_resource(HomePageResource, '/home')
logger.info('HomePageResource endpoint added: /home')

api_v1.add_resource(PostResource, '/post', '/post/<uuid:post_id>')
logger.info('PostResource endpoint added: /post and /post/<uuid:post_id>')

api_v1.add_resource(CommentResource, '/posts/<uuid:post_id>/comments', '/comments/<uuid:comment_id>')
logger.info('CommentResource endpoint added: /posts/<uuid:post_id>/comments and /comments/<uuid:comment_id>')
