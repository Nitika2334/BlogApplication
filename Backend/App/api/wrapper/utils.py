from werkzeug.security import generate_password_hash, check_password_hash
from .schema import get_user_by_username, get_user_by_email, add_user, get_post_by_id, create_post, update_post, delete_post
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt, jwt_required
import datetime
import re

REVOKED_TOKENS = set()

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
            return {
                'message': 'Please provide name, email, and password.',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40001'}
            }, 400

        if not validate_email(email):
            return {
                'message': 'Email format is invalid.',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40013'}
            }, 400

        if not validate_password(password):
            return {
                'message': 'Invalid field value: password.',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40011'}
            }, 400

        existing_user = get_user_by_username(username)
        if existing_user:
            return {
                'message': 'User already exists.',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40002'}
            }, 400

        existing_email = get_user_by_email(email)
        if existing_email:
            return {
                'message': 'User already exists.',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40002'}
            }, 400

        hashed_password = generate_password_hash(password)
        new_user = add_user(username, email, hashed_password)

        expires = datetime.timedelta(minutes=30)
        access_token = create_access_token(identity=new_user.uid, expires_delta=expires)

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
        return {
            'message': f'Registration failed: {str(e)}',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '50000'}
        }, 400

def login(data):
    username = data.get('username')
    password = data.get('password')
    try:
        user = get_user_by_username(username)

        if user and check_password_hash(user.password, password):
            user_id = str(user.uid)
            expires = datetime.timedelta(minutes=30)
            access_token = create_access_token(identity=user.uid, expires_delta=expires)
            response_data = {
                'message': 'User logged in successfully',
                'status': True,
                'type': 'success_message',
                'error_status': {'error_code': '00000'},
                'data': {
                    'user_id': user_id,
                    'username': user.username,
                    'access_token': access_token
                }
            }
            return response_data, 200
        else:
            response_data = {
                'message': 'Invalid credentials',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40100'},
                'error': 'Invalid username or password'
            }
            return response_data, 401
    except Exception as e:
        response_data = {
            'message': 'Login failed',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '50000'},
            'error': str(e)
        }
        return response_data, 500

@jwt_required()
def logout():
    try:
        jti = get_jwt()['jti']
        REVOKED_TOKENS.add(jti)

        response_data = {
            'message': 'User logged out successfully',
            'status': True,
            'type': 'success_message',
            'error_status': {'error_code': '00000'}
        }
        return response_data, 200
    except Exception as e:
        response_data = {
            'message': 'Logout failed',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '50000'},
            'error': str(e)
        }
        return response_data, 500

def is_token_revoked(jwt_payload):
    jti = jwt_payload['jti']
    return jti in REVOKED_TOKENS

@jwt_required()
def create_new_post(data):
    try:
        title = data.get('title')
        content = data.get('content')
        user_id = get_jwt_identity()

        if not title or not content:
            return {
                'message': 'Missing data.',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40001'}
            }, 400

        new_post = create_post(title, content, user_id)

        return {
            'message': 'Post created successfully.',
            'status': True,
            'type': 'success_message',
            'error_status': {'error_code': '00000'},
            'data': {
                'post_id': new_post.id,
                'title': new_post.title,
                'content': new_post.content,
                'author': new_post.author,
                'created_at': new_post.created_at
            }
        }, 200
    except Exception as e:
        return {
            'message': f'Failed to create post: {str(e)}',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40000'}
        }, 400

@jwt_required()
def fetch_post(post_id):
    try:
        post = get_post_by_id(post_id)
        if not post:
            return {
                'message': 'Post not found.',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40020'}
            }, 404

        return {
            'message': 'Post retrieved successfully.',
            'status': True,
            'type': 'success_message',
            'error_status': {'error_code': '00000'},
            'data': {
                'post': {
                    'post_id': post.id,
                    'title': post.title,
                    'content': post.content,
                    'author': post.author,
                    'created_at': post.created_at
                }
            }
        }, 200
    except Exception as e:
        return {
            'message': f'Failed to retrieve post: {str(e)}',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40000'}
        }, 400

@jwt_required()
def update_existing_post(post_id, data):
    try:
        title = data.get('title')
        content = data.get('content')

        post = get_post_by_id(post_id)
        if not post:
            return {
                'message': 'Post not found.',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40020'}
            }, 404

        updated_post = update_post(post_id, title, content)

        return {
            'message': 'Post updated successfully.',
            'status': True,
            'type': 'success_message',
            'error_status': {'error_code': '00000'},
            'data': {
                'post_id': updated_post.id,
                'title': updated_post.title,
                'content': updated_post.content,
                'author': updated_post.author,
                'updated_at': updated_post.updated_at
            }
        }, 200
    except Exception as e:
        return {
            'message': f'Failed to update post: {str(e)}',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40000'}
        }, 400

@jwt_required()
def delete_existing_post(post_id):
    try:
        post = get_post_by_id(post_id)
        if not post:
            return {
                'message': 'Post not found.',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40020'}
            }, 404

        delete_post(post_id)

        return {
            'message': 'Post deleted successfully.',
            'status': True,
            'type': 'success_message',
            'error_status': {'error_code': '00000'}
        }, 200
    except Exception as e:
        return {
            'message': f'Failed to delete post: {str(e)}',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40000'}
        }, 400
