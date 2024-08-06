from flask import request
from flask_restful import Resource
from App.api.wrapper.utils import user_register, user_login, user_logout
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
