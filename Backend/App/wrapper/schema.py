from App.Models.User.UserModel import User
from App import db

def get_user_by_username(username):
    
    try:
        user = User.query.filter_by(username=username).first()
        return user
    except Exception as e:
        raise Exception(f"Database error: {str(e)}")
