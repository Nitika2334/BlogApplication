from werkzeug.security import generate_password_hash, check_password_hash
from .schema import get_user_by_username, get_user_by_email, add_user,create_post,get_post_by_id,update_post,delete_post
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt, jwt_required
import datetime
import re
import time

REVOKED_TOKENS = {}

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
                'access_token':access_token,
                'username': new_user.username,
                'email': new_user.email
            }
        }, 200
    except Exception:
        return {
            'message': 'Registration failed',
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
                'error_status': {'error_code': '40004'}
            }
            return response_data, 400
    except Exception:
        response_data = {
            'message': 'Login failed',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40000'}
        }
        return response_data, 400


def user_logout():
    try:
        jti = get_jwt()['jti']
        exp = get_jwt()['exp']  
        REVOKED_TOKENS[jti] = exp

        response_data = {
            'message': 'User logged out successfully',
            'status': True,
            'type': 'success_message',
            'error_status': {'error_code': '00000'}
        }
        return response_data, 200
    except Exception:
        
        response_data = {
            'message': 'Logout failed',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40005'}
        }
        return response_data, 400

def is_token_revoked(jwt_payload):
    jti = jwt_payload['jti']
    now = time.time()

    # Clean up expired tokens
    for token, exp in list(REVOKED_TOKENS.items()):
        if exp < now:
            del REVOKED_TOKENS[token]

    return jti in REVOKED_TOKENS

def post_to_dict(post):
    return {
        'uid': str(post.uid),
        'title': post.title,
        'content': post.content,
        'user_uid': str(post.user_uid),
        'created_at': post.created_at.isoformat(),
        'updated_at': post.updated_at.isoformat(),
    }

def create_new_post(data):
    try:
        title = data.get('title')
        content = data.get('content')
        user_uid=get_jwt_identity()
        #user_uid = data.get('user_uid')  

        if not title or not content:
            return {
                'message': 'Title and content are required.',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40001'}
            }, 400

        new_post = create_post(title, content, user_uid)

        return {
            'message': 'Post created successfully.',
            'status': True,
            'type': 'success_message',
            'error_status': {'error_code': '00000'},
            'data': post_to_dict(new_post)
        }, 200
    except Exception as e:
        return {
            'message': f'Failed to create post: {str(e)}',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40004'}
        }, 400

def fetch_post(post_id):
    
    try:
        post = get_post_by_id(post_id)
        if not post:
            return {
                'message': 'Post not found',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40006'}
            }, 404

        return {
            'message': 'Post retrieved successfully.',
            'status': True,
            'type': 'success_message',
            'error_status': {'error_code': '00000'},
            'data': post_to_dict(post)
        }, 200
    except Exception as e:
        return {
            'message': f'Failed to retrieve post: {str(e)}',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40005'}
        }, 400

def update_existing_post(post_id, data):
    try:
        title = data.get('title')
        content = data.get('content')
        user_id = get_jwt_identity()  

        if not title and not content:
            return {
                'message': 'Title or content is required.',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40007'}
            }, 400

        post = get_post_by_id(post_id)

        if not post:
            return {
                'message': 'Post not found',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40008'}
            }, 404

        # Check if the current user is the owner of the post
        if str(post.user_uid) != user_id:
            return {
                'message': 'You are not authorized to update this post.',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40006'}
            }, 400

        success = update_post(post_id, title, content)

        if success:
            return {
                'message': 'Post updated successfully.',
                'status': True,
                'type': 'success_message',
                'error_status': {'error_code': '00000'}
            }, 200
        else:
            return {
                'message': 'Failed to update post.',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40009'}
            }, 400
    except Exception as e:
        return {
            'message': f'Failed to update post: {str(e)}',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40009'}
        }, 400


def delete_existing_post(post_id, user_id):
    try:
        post = get_post_by_id(post_id)

        if not post:
            return {
                'message': 'Post not found',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40008'}
            }, 404

        if str(post.user_uid) != user_id:
            return {
                'message': 'You are not authorized to delete this post.',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40006'}
            }, 400

        success = delete_post(post_id, user_id)
        if success:
            return {
                'message': 'Post deleted successfully.',
                'status': True,
                'type': 'success_message',
                'error_status': {'error_code': '00000'}
            }, 200
        else:
            return {
                'message': 'Failed to delete post.',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40010'}
            }, 400
    except Exception as e:
        return {
            'message': f'Failed to delete post: {str(e)}',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40011'}
        }, 400