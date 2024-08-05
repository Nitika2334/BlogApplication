from flask import request, jsonify
from flask_restful import Resource
from .utils import login, logout
from flask_jwt_extended import jwt_required

class SomeProtectedResource(Resource):
    @jwt_required()
    def get(self):
        return {'message': 'This is a protected endpoint.'}, 200

class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        response_data, status_code = login(data)
        return response_data, status_code
    
class LogoutResource(Resource):
    @jwt_required()
    def post(self):
        response_data, status_code = logout()
        return response_data, status_code
    

