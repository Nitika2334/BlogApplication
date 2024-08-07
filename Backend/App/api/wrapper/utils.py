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
    update_post as schema_update_post, delete_post as schema_delete_post
)
from App.api.logger import info_logger, error_logger

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
            error_logger('user_register', 'Missing username, email, or password', data=data)
            return {
                'message': 'Please provide username, email, and password.',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40001'}
            }, 400

        if not validate_email(email):
            error_logger('user_register', 'Invalid email format', email=email)
            return {
                'message': 'Email format is invalid.',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40013'}
            }, 400

        if not validate_password(password):
            error_logger('user_register', 'Password does not meet criteria', password=password)
            return {
                'message': 'Password does not meet criteria.',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40011'}
            }, 400

        if get_user_by_username(username):
            error_logger('user_register', 'Username already exists', username=username)
            return {
                'message': 'Username already exists.',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40002'}
            }, 400

        if get_user_by_email(email):
            error_logger('user_register', 'Email already exists', email=email)
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

        info_logger('user_register', 'User registered successfully', user_id=str(new_user.uid), username=new_user.username)
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
        error_logger('user_register', 'Registration failed', error=str(e))
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
            info_logger('user_login', 'User logged in successfully', user_id=user_id)
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
            error_logger('user_login', 'Invalid credentials', username=username)
            return {
                'message': 'Invalid credentials',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40004'}
            }, 400
    except Exception as e:
        error_logger('user_login', 'Login failed', error=str(e))
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

        info_logger('user_logout', 'User logged out successfully', jti=jti)
        return {
            'message': 'User logged out successfully',
            'status': True,
            'type': 'success_message',
            'error_status': {'error_code': '00000'}
        }, 200
    except Exception as e:
        error_logger('user_logout', 'Logout failed', error=str(e))
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

    return jti in REVOKED_TOKENS

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
            error_logger('create_comment', 'Content is required', data=data)
            return {
                'message': 'Content is required',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40012'}
            }, 400
        
        new_comment = create_new_comment(post_uid, user_uid, content)
        info_logger('create_comment', 'Comment created successfully', comment_id=str(new_comment.uid), post_id=post_uid, user_id=user_uid)
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
        }, 200
    except Exception as e:
        error_logger('create_comment', 'Failed to create comment', error=str(e))
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
        info_logger('get_comments', 'Comments retrieved successfully', post_id=post_uid)
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
        error_logger('get_comments', 'Failed to get comments', error=str(e))
        return {
            'message': f'Failed to get comments: {str(e)}',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40014'}
        }, 400

def update_comment(data, comment_uid, user_uid):
    try:
        content = data.get('content')
        if not content:
            error_logger('update_comment', 'Content is required', data=data)
            return {
                'message': 'Content is required',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40012'}
            }, 400

        existing_comment = update_existing_comment(comment_uid, content, user_uid)
        info_logger('update_comment', 'Comment updated successfully', comment_id=comment_uid, user_id=user_uid)
        return {
            'message': 'Comment updated successfully',
            'status': True,
            'type': 'success_message',
            'error_status': {'error_code': '00000'},
            'data': {
                'comment_id': comment_uid,
                'content': existing_comment.content,
                'updated_at': str(existing_comment.updated_at)
            }
        }, 200
    except Exception as e:
        error_logger('update_comment', 'Failed to update comment', error=str(e))
        return {
            'message': f'Failed to update comment: {str(e)}',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40015'}
        }, 400

def delete_comment(comment_uid, user_uid):
    try:
        delete_existing_comment(comment_uid, user_uid)
        info_logger('delete_comment', 'Comment deleted successfully', comment_id=comment_uid, user_id=user_uid)
        return {
            'message': 'Comment deleted successfully',
            'status': True,
            'type': 'success_message',
            'error_status': {'error_code': '00000'}
        }, 200
    except Exception as e:
        error_logger('delete_comment', 'Failed to delete comment', error=str(e))
        return {
            'message': f'Failed to delete comment: {str(e)}',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40016'}
        }, 400

# Posts

def create_post(data, user_uid):
    try:
        title = data.get('title')
        content = data.get('content')
        if not title or not content:
            error_logger('create_post', 'Title and content are required', data=data)
            return {
                'message': 'Title and content are required',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40017'}
            }, 400

        post = schema_create_post(user_uid, title, content)
        info_logger('create_post', 'Post created successfully', post_id=str(post.uid), user_id=user_uid)
        return {
            'message': 'Post created successfully',
            'status': True,
            'type': 'success_message',
            'error_status': {'error_code': '00000'},
            'data': {
                'post_id': str(post.uid),
                'title': post.title,
                'content': post.content,
                'created_at': str(post.created_at)
            }
        }, 200
    except Exception as e:
        error_logger('create_post', 'Failed to create post', error=str(e))
        return {
            'message': f'Failed to create post: {str(e)}',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40018'}
        }, 400

def get_post(post_uid):
    try:
        post = schema_get_post_by_id(post_uid)
        if post:
            info_logger('get_post', 'Post retrieved successfully', post_id=post_uid)
            return {
                'message': 'Post retrieved successfully',
                'status': True,
                'type': 'success_message',
                'error_status': {'error_code': '00000'},
                'data': {
                    'post_id': str(post.uid),
                    'title': post.title,
                    'content': post.content,
                    'created_at': str(post.created_at),
                    'updated_at': str(post.updated_at)
                }
            }, 200
        else:
            error_logger('get_post', 'Post not found', post_id=post_uid)
            return {
                'message': 'Post not found',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40019'}
            }, 404
    except Exception as e:
        error_logger('get_post', 'Failed to get post', error=str(e))
        return {
            'message': f'Failed to get post: {str(e)}',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40020'}
        }, 400

def update_post(data, post_uid, user_uid):
    try:
        title = data.get('title')
        content = data.get('content')
        if not title or not content:
            error_logger('update_post', 'Title and content are required', data=data)
            return {
                'message': 'Title and content are required',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40017'}
            }, 400

        updated_post = schema_update_post(post_uid, title, content, user_uid)
        info_logger('update_post', 'Post updated successfully', post_id=post_uid, user_id=user_uid)
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
        error_logger('update_post', 'Failed to update post', error=str(e))
        return {
            'message': f'Failed to update post: {str(e)}',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40021'}
        }, 400

def delete_post(post_uid, user_uid):
    try:
        schema_delete_post(post_uid, user_uid)
        info_logger('delete_post', 'Post deleted successfully', post_id=post_uid, user_id=user_uid)
        return {
            'message': 'Post deleted successfully',
            'status': True,
            'type': 'success_message',
            'error_status': {'error_code': '00000'}
        }, 200
    except Exception as e:
        error_logger('delete_post', 'Failed to delete post', error=str(e))
        return {
            'message': f'Failed to delete post: {str(e)}',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40022'}
        }, 400

def get_paginated_posts(page, per_page):
    try:
        posts = schema_get_paginated_posts(page, per_page)
        posts_list = [{
            'post_id': str(post.uid),
            'title': post.title,
            'content': post.content,
            'created_at': str(post.created_at),
            'updated_at': str(post.updated_at)
        } for post in posts]

        info_logger('get_paginated_posts', 'Posts retrieved successfully', page=page, per_page=per_page)
        return {
            'message': 'Posts retrieved successfully',
            'status': True,
            'type': 'success_message',
            'error_status': {'error_code': '00000'},
            'data': {
                'posts': posts_list
            }
        }, 200
    except Exception as e:
        error_logger('get_paginated_posts', 'Failed to get posts', error=str(e))
        return {
            'message': f'Failed to get posts: {str(e)}',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40023'}
        }, 400
