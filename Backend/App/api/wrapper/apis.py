from flask import request
from flask_restful import Resource
from App.api.wrapper.utils import user_register, user_login, user_logout, get_comments, create_comment, update_comment, delete_comment
from flask_jwt_extended import jwt_required, get_jwt_identity

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
        

class CommentResource(Resource):
    @jwt_required()
    def get(self, post_id):
        try:
            if post_id is None:
                return {
                'message': 'Post ID is required',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40006'}
            }, 400

            response_data, status_code = get_comments(post_id)
            return response_data, status_code
        except Exception:
            return {
                'message': 'Failed to get comments',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40005'},
            }, 400
        
    @jwt_required()
    def post(self, post_id):
        try:
            if post_id is None:
                return {
                'message': 'Post ID is required',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40006'}
            }, 400
            
            user_id = get_jwt_identity()
            data = request.get_json()
            response_data, status_code = create_comment(data, post_id, user_id)
            return response_data, status_code
        except Exception:
            return {
                'message': 'Failed to create comment',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40005'}
            }, 400

    @jwt_required()
    def put(self, comment_id):
        try:
            if comment_id is None:
                return {
                    'message': 'Comment ID is required',
                    'status': False,
                    'type': 'custom_error',
                    'error_status': {'error_code': '40006'}
                    }, 400
            
            data = request.get_json()
            response_data, status_code = update_comment(data, comment_id)
            return response_data, status_code
        except Exception:
            return {
                'message': 'Failed to update comment',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40005'},
            }, 400

    @jwt_required()
    def delete(self, comment_id):
        try:
            if comment_id is None:
                return {
                'message': 'Comment ID is required',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40006'}
                }, 400
            
            user_id = get_jwt_identity()
            response_data, status_code = delete_comment(comment_id, user_id)
            return response_data, status_code
        except Exception:
            return {
                'message': 'Failed to delete comment',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40005'},
            }, 400