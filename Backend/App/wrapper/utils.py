from werkzeug.security import check_password_hash
from .schema import get_user_by_username
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity, get_jwt, create_access_token, jwt_required
import datetime

REVOKED_TOKENS = set()

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