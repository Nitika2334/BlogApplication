from flask import request
from flask_restful import Resource
from App.api.wrapper.utils import user_register, user_login, user_logout, get_comments, create_comment, update_comment, delete_comment
from flask_jwt_extended import jwt_required, get_jwt_identity
from App.api.logger import logger

from App.api.wrapper.utils import (
    create_post, 
    get_post_by_id, 
    update_post, 
    delete_post, 
    get_home_page_data
)

class SomeProtectedResource(Resource):
    @jwt_required()
    def get(self):
        logger.info('Accessed protected endpoint')
        return {'message': 'This is a protected endpoint.'}, 200

class RegisterResource(Resource):
    def post(self):
        try:
            data = request.get_json()
            logger.info('Registration attempt with data: %s', data)
            response_data, status_code = user_register(data)
            logger.info('Registration response: %s', response_data)
            return response_data, status_code
        except Exception as e:
            logger.error('Registration failed: %s', str(e))
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
            logger.info('Login attempt with data: %s', data)
            response_data, status_code = user_login(data)
            logger.info('Login response: %s', response_data)
            return response_data, status_code
        except Exception as e:
            logger.error('Login failed: %s', str(e))
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
            logger.info('Logout attempt for user: %s', get_jwt_identity())
            response_data, status_code = user_logout()
            logger.info('Logout response: %s', response_data)
            return response_data, status_code
        except Exception as e:
            logger.error('Logout failed: %s', str(e))
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
                logger.warning('Post ID is required for getting comments')
                return {
                    'message': 'Post ID is required',
                    'status': False,
                    'type': 'custom_error',
                    'error_status': {'error_code': '40006'}
                }, 400

            logger.info('Fetching comments for post_id: %s', post_id)
            response_data, status_code = get_comments(post_id)
            logger.info('Fetched comments response: %s', response_data)
            return response_data, status_code
        except Exception as e:
            logger.error('Failed to get comments: %s', str(e))
            return {
                'message': f'Failed to get comments: {str(e)}',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40005'}
            }, 400

    @jwt_required()
    def post(self, post_id):
        try:
            if post_id is None:
                logger.warning('Post ID is required for creating comment')
                return {
                    'message': 'Post ID is required',
                    'status': False,
                    'type': 'custom_error',
                    'error_status': {'error_code': '40006'}
                }, 400

            user_id = get_jwt_identity()
            data = request.get_json()
            logger.info('Creating comment for post_id: %s with data: %s', post_id, data)
            response_data, status_code = create_comment(data, post_id, user_id)
            logger.info('Created comment response: %s', response_data)
            return response_data, status_code
        except Exception as e:
            logger.error('Failed to create comment: %s', str(e))
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
                logger.warning('Comment ID is required for updating comment')
                return {
                    'message': 'Comment ID is required',
                    'status': False,
                    'type': 'custom_error',
                    'error_status': {'error_code': '40006'}
                }, 400

            data = request.get_json()
            user_id = get_jwt_identity()
            logger.info('Updating comment_id: %s with data: %s', comment_id, data)
            response_data, status_code = update_comment(data, comment_id, user_id)
            logger.info('Updated comment response: %s', response_data)
            return response_data, status_code
        except Exception as e:
            logger.error('Failed to update comment: %s', str(e))
            return {
                'message': f'Failed to update comment: {str(e)}',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40005'}
            }, 400

    @jwt_required()
    def delete(self, comment_id):
        try:
            if comment_id is None:
                logger.warning('Comment ID is required for deleting comment')
                return {
                    'message': 'Comment ID is required',
                    'status': False,
                    'type': 'custom_error',
                    'error_status': {'error_code': '40006'}
                }, 400

            user_id = get_jwt_identity()
            logger.info('Deleting comment_id: %s', comment_id)
            response_data, status_code = delete_comment(comment_id, user_id)
            logger.info('Deleted comment response: %s', response_data)
            return response_data, status_code
        except Exception as e:
            logger.error('Failed to delete comment: %s', str(e))
            return {
                'message': f'Failed to delete comment: {str(e)}',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40005'}
            }, 400

class PostResource(Resource):
    @jwt_required()
    def post(self):
        try:
            data = request.get_json()
            logger.info('Creating new post with data: %s', data)
            response_data, status_code = create_post(data)
            logger.info('Created post response: %s', response_data)
            return response_data, status_code
        except Exception as e:
            logger.error('Error creating post: %s', str(e))
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
                logger.warning('Post ID is required for updating post')
                return {
                    'message': 'Post ID is required',
                    'status': False,
                    'type': 'custom_error',
                    'error_status': {'error_code': '40006'}
                }, 400

            data = request.get_json()
            logger.info('Updating post_id: %s with data: %s', post_id, data)
            response_data, status_code = update_post(post_id, data)
            logger.info('Updated post response: %s', response_data)
            return response_data, status_code
        except Exception as e:
            logger.error('Failed to update post: %s', str(e))
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
                logger.warning('Post ID is required for fetching post')
                return {
                    'message': 'Post ID is required',
                    'status': False,
                    'type': 'custom_error',
                    'error_status': {'error_code': '40006'}
                }, 400

            logger.info('Fetching post with post_id: %s', post_id)
            response_data, status_code = get_post_by_id(post_id)
            logger.info('Fetched post response: %s', response_data)
            return response_data, status_code
        except Exception as e:
            logger.error('Failed to get post: %s', str(e))
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
                logger.warning('Post ID is required for deleting post')
                return {
                    'message': 'Post ID is required',
                    'status': False,
                    'type': 'custom_error',
                    'error_status': {'error_code': '40006'}
                }, 400

            user_id = get_jwt_identity()
            logger.info('Deleting post with post_id: %s', post_id)
            response_data, status_code = delete_post(post_id, user_id)
            logger.info('Deleted post response: %s', response_data)
            return response_data, status_code
        except Exception as e:
            logger.error('Failed to delete post: %s', str(e))
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
            user_id = request.args.get('user')

            logger.info('Fetching home page data with page: %d, size: %d, user_id: %s', page, size, user_id)
            response_data, status_code = get_home_page_data(page, size, user_id)
            logger.info('Fetched home page data response: %s', response_data)
            return response_data, status_code
        except Exception as e:
            logger.error('Failed to retrieve home page data: %s', str(e))
            return {
                'message': f'Failed to retrieve home page data: {str(e)}',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40016'}
            }, 400

