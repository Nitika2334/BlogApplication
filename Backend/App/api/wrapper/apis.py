from flask import request
from flask_restful import Resource
from App.api.wrapper.utils import user_register, user_login, user_logout, get_comments, create_comment, update_comment, delete_comment
from flask_jwt_extended import jwt_required, get_jwt_identity
from App.api.logger import info_logger, error_logger, log_error
from App.api.wrapper.utils import (
    create_new_post, 
    get_post, 
    update_post, 
    delete_post, 
    get_home_page_data
)

class SomeProtectedResource(Resource):
    @jwt_required()
    def get(self):
        try:
            info_logger('SomeProtectedResource', 'Accessed protected endpoint')
            return {'message': 'This is a protected endpoint.'}, 200
        except Exception as e:
            error_logger('SomeProtectedResource', 'Failed to access protected endpoint', error=str(e))
            return {'message': 'Internal Server Error'}, 500
class RegisterResource(Resource):
    def post(self):
        try:
            data = request.get_json()
            info_logger('RegisterResource', 'Register request received', data=data)
            response_data, status_code = user_register(data)
            return response_data, status_code
        except Exception as e:
            error_logger('RegisterResource', 'Registration failed', error=str(e))
            return {
                'message': f'Registration failed: {str(e)}',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40003'}
            }, 400

class LoginResource(Resource):
    def post(self):
        try:
            data = request.get_json()
            info_logger('LoginResource', 'Login request received', data=data)
            response_data, status_code = user_login(data)
            return response_data, status_code
        except Exception as e:
            error_logger('LoginResource', 'Login failed', error=str(e))
            return {
                'message': f'Login failed: {str(e)}',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40003'}
            }, 400

class LogoutResource(Resource):
    @jwt_required()
    def post(self):
        try:
            info_logger('LogoutResource', 'Logout request received')
            response_data, status_code = user_logout()
            return response_data, status_code
        except Exception as e:
            error_logger('LogoutResource', 'Logout failed', error=str(e))
            return {
                'message': f'Logout failed: {str(e)}',
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

            info_logger('CommentResource', 'Get comments request received', post_id=post_id)
            response_data, status_code = get_comments(post_id)
            return response_data, status_code
        except Exception as e:
            error_logger('CommentResource', 'Failed to get comments', post_id=post_id, error=str(e))
            return {
                'message': f'Failed to get comments: {str(e)}',
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
            info_logger('CommentResource', 'Create comment request received', post_id=post_id, data=data, user_id=user_id)
            response_data, status_code = create_comment(data, post_id, user_id)
            return response_data, status_code
        except Exception as e:
            error_logger('CommentResource', 'Failed to create comment', post_id=post_id, error=str(e))
            return {
                'message': f'Failed to create comment: {str(e)}',
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
            user_id = get_jwt_identity()
            info_logger('CommentResource', 'Update comment request received', comment_id=comment_id, data=data, user_id=user_id)
            response_data, status_code = update_comment(data, comment_id, user_id)
            return response_data, status_code
        except Exception as e:
            error_logger('CommentResource', 'Failed to update comment', comment_id=comment_id, error=str(e))
            return {
                'message': f'Failed to update comment: {str(e)}',
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
            info_logger('CommentResource', 'Delete comment request received', comment_id=comment_id, user_id=user_id)
            response_data, status_code = delete_comment(comment_id, user_id)
            return response_data, status_code
        except Exception as e:
            error_logger('CommentResource', 'Failed to delete comment', comment_id=comment_id, error=str(e))
            return {
                'message': f'Failed to delete comment: {str(e)}',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40005'},
            }, 400
        
class PostResource(Resource):
    @jwt_required()
    def post(self):
        try:
            data = request.get_json()
            info_logger('PostResource', 'Create post request received', data=data)
            response_data, status_code = create_new_post(data)
            return response_data, status_code
        except Exception as e:
            error_logger('PostResource', 'Error creating post', error=str(e))
            return {
                'message': f'Error creating post: {str(e)}',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40000'}
            }, 400

    @jwt_required()
    def put(self, post_id):
        
        try:
            if post_id is None:
                return {
                    'message': 'Post ID is required',
                    'status': False,
                    'type': 'custom_error',
                    'error_status': {'error_code': '40006'}
                }, 400

            data = request.get_json()
            info_logger('PostResource', 'Update post request received', post_id=post_id, data=data)
            response_data, status_code = update_post(post_id, data)
            return response_data, status_code
        except Exception as e:
            error_logger('PostResource', 'Failed to update post', post_id=post_id, error=str(e))
            return {
                'message': f'Failed to update post: {str(e)}',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40005'}
            }, 400


    @jwt_required()
    def get(self, post_id):
        try:
            if not post_id:
                return {
                    'message': 'Post ID is required',
                    'status': False,
                    'type': 'custom_error',
                    'error_status': {'error_code': '40006'}
                }, 400
            
            info_logger('PostResource', 'Get post request received', post_id=post_id)
            response_data, status_code = get_post(post_id)
            return response_data, status_code
        except Exception as e:
            error_logger('PostResource', 'Failed to get post', post_id=post_id, error=str(e))  
            return {
                'message': f'Failed to get post: {str(e)}',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40005'}
            }, 400


    @jwt_required()
    def delete(self, post_id):
        try:
            if not post_id:
                return {
                    'message': 'Post ID is required',
                    'status': False,
                    'type': 'custom_error',
                    'error_status': {'error_code': '40006'}
                }, 400

            user_id = get_jwt_identity()
            info_logger('PostResource', 'Delete post request received', post_id=post_id, user_id=user_id)
            response_data, status_code = delete_post(post_id, user_id)
            return response_data, status_code
        except Exception as e:
            error_logger('PostResource', 'Failed to delete post', post_id=post_id, error=str(e))
            return {
                'message': f'Failed to delete post: {str(e)}',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40005'}
            }, 400

class HomePageResource(Resource):
    @jwt_required()
    def get(self):
        try:

            page = int(request.args.get('page', 1))
            size = int(request.args.get('size', 10))
            user_id = request.args.get('user', None)  

            if page < 1 or size < 1:
                raise ValueError("Page and size must be positive integers.")
            
            info_logger('HomePageResource', 'Get home page data request received', page=page, size=size, user_id=user_id)
            
            
            response_data, status_code = get_home_page_data(page, size, user_id)
            return response_data, status_code
        
        except ValueError as ve:
            error_logger('HomePageResource', 'Invalid pagination parameters', error=str(ve))
            return {
                'message': f'Invalid pagination parameters: {str(ve)}',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40016'}
            }, 400
        
        except Exception as e:
            error_logger('HomePageResource', 'Failed to retrieve home page data', error=str(e))
            return {
                'message': f'Failed to retrieve home page data: {str(e)}',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40016'}
            }, 400