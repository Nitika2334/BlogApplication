from flask import request
from flask_restful import Resource
from App.api.wrapper.utils import user_register, user_login, user_logout,fetch_post,create_new_post,update_existing_post,delete_existing_post
from flask_jwt_extended import jwt_required

class SomeProtectedResource(Resource):
    @jwt_required()
    def get(self):
        return {'message': 'This is a protected endpoint.'}, 200

class RegisterResource(Resource):
    def post(self):
        try:
            data = request.get_json()
            response_data, status_code = user_register(data)
            return response_data, status_code
        except Exception:
            return {
                'message': 'Registration failed',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40003'}
            }, 400

class LoginResource(Resource):
    def post(self):
        try:
            data = request.get_json()
            response_data, status_code = user_login(data)
            return response_data, status_code
        except Exception:
            return {
                'message': 'Login failed',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40003'}
            }, 400

class LogoutResource(Resource):
    @jwt_required()
    def post(self):
        try:
            response_data, status_code = user_logout()
            return response_data, status_code
        except Exception:
            return {
                'message': 'Logout failed',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40003'}
            }, 400
        

class PostResource(Resource):
    @jwt_required()
    def get(self):
        try:
            post_id = request.args.get('id')
            if not post_id:
                return {
                    'message': 'Post ID is required.',
                    'status': False,
                    'type': 'custom_error',
                    'error_status': {'error_code': '40010', 'error_message': 'Missing required field: post_id'}
                }, 400
            data = {'post_id': post_id}
            response_data, status_code = fetch_post(data)
            if status_code == 404:
                return {
                    'message': 'Post not found.',
                    'status': False,
                    'type': 'resource_error',
                    'error_status': {'error_code': '40020'}
                }, 404
            return response_data, status_code
        except Exception as e:
            return {
                'message': 'Internal server error. Please try again later.',
                'status': False,
                'type': 'internal_error',
                'error_status': {'error_code': '40000', 'error_message': str(e)}
            }, 400

    @jwt_required()
    def post(self):
        try:
            data = request.get_json()
            if not data.get('name') or not data.get('email') or not data.get('password'):
                return {
                    'message': 'Please provide name, email, and password.',
                    'status': False,
                    'type': 'validation_error',
                    'error_status': {'error_code': '40001'}
                }, 400
            response_data, status_code = create_new_post(data)
            return response_data, status_code
        except Exception as e:
            return {
                'message': 'Internal server error. Please try again later.',
                'status': False,
                'type': 'internal_error',
                'error_status': {'error_code': '40000', 'error_message': str(e)}
            }, 400

    @jwt_required()
    def patch(self):
        try:
            data = request.get_json()
            post_id = data.get('post_id')
            title = data.get('title')
            content = data.get('content')
            if not post_id or not title or not content:
                return {
                    'message': 'Post ID, title, and content are required.',
                    'status': False,
                    'type': 'validation_error',
                    'error_status': {'error_code': '40010', 'error_message': 'Missing required field(s): post_id, title, content'}
                }, 400
            response_data, status_code = update_existing_post(post_id, title, content)
            if status_code == 404:
                return {
                    'message': 'Post not found.',
                    'status': False,
                    'type': 'resource_error',
                    'error_status': {'error_code': '40020'}
                }, 404
            return response_data, status_code
        except Exception as e:
            return {
                'message': 'Internal server error. Please try again later.',
                'status': False,
                'type': 'internal_error',
                'error_status': {'error_code': '40000', 'error_message': str(e)}
            }, 400

    @jwt_required()
    def delete(self):
        try:
            data = request.get_json()
            post_id = data.get('post_id')
            if not post_id:
                return {
                    'message': 'Post ID is required.',
                    'status': False,
                    'type': 'validation_error',
                    'error_status': {'error_code': '40010', 'error_message': 'Missing required field: post_id'}
                }, 400
            response_data, status_code = delete_existing_post(post_id)
            if status_code == 404:
                return {
                    'message': 'Post not found.',
                    'status': False,
                    'type': 'resource_error',
                    'error_status': {'error_code': '40020'}
                }, 404
            return response_data, status_code
        except Exception as e:
            return {
                'message': 'Internal server error. Please try again later.',
                'status': False,
                'type': 'internal_error',
                'error_status': {'error_code': '40000', 'error_message': str(e)}
            }, 400

