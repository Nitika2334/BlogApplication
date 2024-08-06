from werkzeug.security import generate_password_hash, check_password_hash
from .schema import get_user_by_username, get_user_by_email, add_user
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