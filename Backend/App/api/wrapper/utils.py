import os
import re
import datetime
import time
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt
from flask import request, current_app, jsonify
from .schema import (
    get_user_by_username, get_user_by_email, add_user, create_new_comment, 
    get_comments_by_post_id, update_existing_comment, delete_existing_comment,
    create_post as schema_create_post, get_post_by_id as schema_get_post_by_id, 
    update_post as schema_update_post, delete_post as schema_delete_post, 
    get_paginated_posts as schema_get_paginated_posts
)
from App.api.logger import logger  # Assuming logger is set up in App/logger.py

REVOKED_TOKENS = {}

# Utility Functions

def validate_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email)

def validate_password(password):
    password_regex = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    return re.match(password_regex, password)

def user_register(data):
    try:
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            logger.warning('Missing registration fields: username, email, or password.')
            return {
                'message': 'Please provide username, email, and password.',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40001'}
            }, 400

        if not validate_email(email):
            logger.warning('Invalid email format: %s', email)
            return {
                'message': 'Email format is invalid.',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40013'}
            }, 400

        if not validate_password(password):
            logger.warning('Password does not meet criteria.')
            return {
                'message': 'Password does not meet criteria.',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40011'}
            }, 400

        existing_user = get_user_by_username(username)
        if existing_user:
            logger.warning('Username already exists: %s', username)
            return {
                'message': 'Username already exists.',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40002'}
            }, 400

        existing_email = get_user_by_email(email)
        if existing_email:
            logger.warning('Email already exists: %s', email)
            return {
                'message': 'Email already exists.',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40002'}
            }, 400

        hashed_password = generate_password_hash(password)
        new_user = add_user(username, email, hashed_password)

        expires = datetime.timedelta(minutes=30)
        access_token = create_access_token(identity=new_user.uid, expires_delta=expires)

        logger.info('User registered successfully: %s', username)
        return {
            'message': 'User registered successfully.',
            'status': True,
            'type': 'success_message',
            'error_status': {'error_code': '00000'},
            'data': {
                'user_id': str(new_user.uid),
                'access_token': access_token,
                'username': new_user.username,
                'email': new_user.email
            }
        }, 200
    except Exception as e:
        logger.error('Registration failed: %s', str(e))
        return {
            'message': f'Registration failed: {str(e)}',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40000'}
        }, 400

def user_login(data):
    try:
        username = data.get('username')
        password = data.get('password')
        user = get_user_by_username(username)

        if user and check_password_hash(user.password, password):
            user_id = str(user.uid)
            expires = datetime.timedelta(minutes=120)
            access_token = create_access_token(identity=user.uid, expires_delta=expires)
            logger.info('User logged in successfully: %s', username)
            return {
                'message': 'User logged in successfully',
                'status': True,
                'type': 'success_message',
                'error_status': {'error_code': '00000'},
                'data': {
                    'user_id': user_id,
                    'username': user.username,
                    'access_token': access_token
                }
            }, 200
        else:
            logger.warning('Invalid login credentials for user: %s', username)
            return {
                'message': 'Invalid credentials',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40004'}
            }, 400
    except Exception as e:
        logger.error('Login failed: %s', str(e))
        return {
            'message': f'Login failed: {str(e)}',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40000'}
        }, 400

def user_logout():
    try:
        jti = get_jwt()['jti']
        exp = get_jwt()['exp']  
        REVOKED_TOKENS[jti] = exp
        logger.info('User logged out, token revoked: %s', jti)
        return {
            'message': 'User logged out successfully',
            'status': True,
            'type': 'success_message',
            'error_status': {'error_code': '00000'}
        }, 200
    except Exception as e:
        logger.error('Logout failed: %s', str(e))
        return {
            'message': f'Logout failed: {str(e)}',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40005'}
        }, 400

def is_token_revoked(jwt_payload):
    jti = jwt_payload['jti']
    now = time.time()
    for token, exp in list(REVOKED_TOKENS.items()):
        if exp < now:
            del REVOKED_TOKENS[token]

    if jti in REVOKED_TOKENS:
        logger.info('Token is revoked: %s', jti)
        return True

    return False

# Comments

def comment_to_dict(comment):
    return {
        'uid': str(comment.uid),
        'content': comment.content,
        'user_uid': str(comment.user_uid),
        'post_uid': str(comment.post_uid),
        'created_at': comment.created_at.isoformat(),
        'updated_at': comment.updated_at.isoformat(),
    }

def create_comment(data, post_uid, user_uid):
    try:
        content = data.get('content')
        if not content:
            logger.warning('Content is required for creating comment.')
            return {
                'message': 'Content is required',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40012'}
            }, 400
        
        new_comment = create_new_comment(post_uid, user_uid, content)
        logger.info('Comment created successfully for post: %s', post_uid)
        return {
            'message': 'Comment created successfully',
            'status': True,
            'type': 'success_message',
            'error_status': {'error_code': '00000'},
            'data': {
                'comment_id': str(new_comment.uid),
                'post_id': str(post_uid),
                'user_id': str(user_uid),
                'content': new_comment.content,
                'created_at': str(new_comment.created_at)
            }
        }, 201
    except Exception as e:
        logger.error('Failed to create comment: %s', str(e))
        return {
            'message': f'Failed to create comment: {str(e)}',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40013'}
        }, 400
    
def get_comments(post_uid):
    try:
        comments = get_comments_by_post_id(post_uid)
        comments_list = [comment_to_dict(comment) for comment in comments]
        logger.info('Comments retrieved successfully for post: %s', post_uid)
        return {
            'message': 'Comments retrieved successfully',
            'status': True,
            'type': 'success_message',
            'error_status': {'error_code': '00000'},
            'data': {
                'comments': comments_list
            }
        }, 200
    except Exception as e:
        logger.error('Failed to get comments: %s', str(e))
        return {
            'message': f'Failed to get comments: {str(e)}',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40014'}
        }, 400
    
def update_comment(data, comment_id, user_id):
    try:
        content = data.get('content')
        if not content:
            logger.warning('Content is required to update comment.')
            return {
                'message': 'Content is required',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40012'}
            }, 400
        
        updated_comment = update_existing_comment(comment_id, user_id, content)
        if not updated_comment:
            logger.warning('Comment not found or user unauthorized to update comment: %s', comment_id)
            return {
                'message': 'Comment not found or user unauthorized to update comment',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40015'}
            }, 404
        
        logger.info('Comment updated successfully: %s', comment_id)
        return {
            'message': 'Comment updated successfully',
            'status': True,
            'type': 'success_message',
            'error_status': {'error_code': '00000'},
            'data': {
                'comment_id': str(updated_comment.uid),
                'content': updated_comment.content,
                'updated_at': str(updated_comment.updated_at)
            }
        }, 200
    except Exception as e:
        logger.error('Failed to update comment: %s', str(e))
        return {
            'message': f'Failed to update comment: {str(e)}',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40016'}
        }, 400

def delete_comment(comment_id, user_id):
    try:
        success = delete_existing_comment(comment_id, user_id)
        if not success:
            logger.warning('Comment not found or user unauthorized to delete comment: %s', comment_id)
            return {
                'message': 'Comment not found or user unauthorized to delete comment',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40017'}
            }, 404
        
        logger.info('Comment deleted successfully: %s', comment_id)
        return {
            'message': 'Comment deleted successfully',
            'status': True,
            'type': 'success_message',
            'error_status': {'error_code': '00000'}
        }, 200
    except Exception as e:
        logger.error('Failed to delete comment: %s', str(e))
        return {
            'message': f'Failed to delete comment: {str(e)}',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40018'}
        }, 400

# Posts

def post_to_dict(post):
    return {
        'uid': str(post.uid),
        'title': post.title,
        'content': post.content,
        'user_uid': str(post.user_uid),
        'created_at': post.created_at.isoformat(),
        'updated_at': post.updated_at.isoformat(),
    }

def create_post(data, user_uid):
    try:
        title = data.get('title')
        content = data.get('content')
        if not title or not content:
            logger.warning('Title and content are required for creating post.')
            return {
                'message': 'Title and content are required',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40019'}
            }, 400

        new_post = schema_create_post(user_uid, title, content)
        logger.info('Post created successfully: %s', new_post.uid)
        return {
            'message': 'Post created successfully',
            'status': True,
            'type': 'success_message',
            'error_status': {'error_code': '00000'},
            'data': {
                'post_id': str(new_post.uid),
                'title': new_post.title,
                'content': new_post.content,
                'user_id': str(new_post.user_uid),
                'created_at': str(new_post.created_at)
            }
        }, 201
    except Exception as e:
        logger.error('Failed to create post: %s', str(e))
        return {
            'message': f'Failed to create post: {str(e)}',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40020'}
        }, 400

def get_posts(page, per_page):
    try:
        posts, total = schema_get_paginated_posts(page, per_page)
        posts_list = [post_to_dict(post) for post in posts]
        logger.info('Posts retrieved successfully, page: %s', page)
        return {
            'message': 'Posts retrieved successfully',
            'status': True,
            'type': 'success_message',
            'error_status': {'error_code': '00000'},
            'data': {
                'posts': posts_list,
                'total': total,
                'page': page,
                'per_page': per_page
            }
        }, 200
    except Exception as e:
        logger.error('Failed to get posts: %s', str(e))
        return {
            'message': f'Failed to get posts: {str(e)}',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40021'}
        }, 400

def get_post_by_id(post_uid):
    try:
        post = schema_get_post_by_id(post_uid)
        if not post:
            logger.warning('Post not found: %s', post_uid)
            return {
                'message': 'Post not found',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40022'}
            }, 404

        logger.info('Post retrieved successfully: %s', post_uid)
        return {
            'message': 'Post retrieved successfully',
            'status': True,
            'type': 'success_message',
            'error_status': {'error_code': '00000'},
            'data': {
                'post': post_to_dict(post)
            }
        }, 200
    except Exception as e:
        logger.error('Failed to get post: %s', str(e))
        return {
            'message': f'Failed to get post: {str(e)}',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40023'}
        }, 400

def update_post(data, post_uid, user_uid):
    try:
        title = data.get('title')
        content = data.get('content')
        if not title or not content:
            logger.warning('Title and content are required to update post.')
            return {
                'message': 'Title and content are required',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40019'}
            }, 400
        
        updated_post = schema_update_post(post_uid, user_uid, title, content)
        if not updated_post:
            logger.warning('Post not found or user unauthorized to update post: %s', post_uid)
            return {
                'message': 'Post not found or user unauthorized to update post',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40024'}
            }, 404

        logger.info('Post updated successfully: %s', post_uid)
        return {
            'message': 'Post updated successfully',
            'status': True,
            'type': 'success_message',
            'error_status': {'error_code': '00000'},
            'data': {
                'post_id': str(updated_post.uid),
                'title': updated_post.title,
                'content': updated_post.content,
                'updated_at': str(updated_post.updated_at)
            }
        }, 200
    except Exception as e:
        logger.error('Failed to update post: %s', str(e))
        return {
            'message': f'Failed to update post: {str(e)}',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40025'}
        }, 400

def delete_post(post_uid, user_uid):
    try:
        success = schema_delete_post(post_uid, user_uid)
        if not success:
            logger.warning('Post not found or user unauthorized to delete post: %s', post_uid)
            return {
                'message': 'Post not found or user unauthorized to delete post',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40026'}
            }, 404
        
        logger.info('Post deleted successfully: %s', post_uid)
        return {
            'message': 'Post deleted successfully',
            'status': True,
            'type': 'success_message',
            'error_status': {'error_code': '00000'}
        }, 200
    except Exception as e:
        logger.error('Failed to delete post: %s', str(e))
        return {
            'message': f'Failed to delete post: {str(e)}',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40027'}
        }, 400

def get_home_page_data(page, size, user_id=None):
    try:
        posts, total_posts = schema_get_paginated_posts(page, size, user_id)

        data = {
            "current_page": page,
            "page_size": size,
            "total_pages": (total_posts + size - 1) // size,
            "total_posts": total_posts,
            "posts": [post_to_dict(post) for post in posts]
        }

        return {
            'message': 'Home page data retrieved successfully.',
            'status': True,
            'type': 'success_message',
            'error_status': {'error_code': '00000'},
            'data': data
        }, 200
    except Exception as e:
        return {
            'message': f'Failed to retrieve home page data: {str(e)}',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40016'}
        }, 400