from flask import request
from flask_restful import Resource
from App.api.wrapper.utils import user_register, login, logout, create_post, fetch_post, update_post, delete_post
from flask_jwt_extended import jwt_required

class SomeProtectedResource(Resource):
    @jwt_required()
    def get(self):
        return {'message': 'This is a protected endpoint.'}, 200

class RegisterResource(Resource):
    def post(self):
        data = request.get_json()
        response_data, status_code = user_register(data)
        return response_data, status_code

class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        response_data, status_code = login(data)
        return response_data, status_code

class LogoutResource(Resource):
    @jwt_required()
    def post(self):
        response_data, status_code = logout()
        return response_data, status_code
    
class PostResource(Resource):
    @jwt_required()
    def get(self):
        post_id = request.args.get('id')
        if not post_id:
            return {
                'message': 'Post ID is required.',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40001'}
            }, 400
        data = {'post_id': post_id}
        response_data, status_code = fetch_post(data)
        return response_data, status_code

    @jwt_required()
    def post(self):
        data = request.get_json()
        response_data, status_code = create_post(data)
        return response_data, status_code

    @jwt_required()
    def patch(self):
        data = request.get_json()
        post_id = data.get('post_id')
        title = data.get('title')
        content = data.get('content')
        if not post_id or not title or not content:
            return {
                'message': 'Post ID, title, and content are required.',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40001'}
            }, 400
        response_data, status_code = update_post(post_id, title, content)
        return response_data, status_code

    @jwt_required()
    def delete(self):
        data = request.get_json()
        post_id = data.get('post_id')
        if not post_id:
            return {
                'message': 'Post ID is required.',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40001'}
            }, 400
        response_data, status_code = delete_post(post_id)
        return response_data, status_code
    