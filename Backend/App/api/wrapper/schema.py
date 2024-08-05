from App.Models.User.UserModel import User
from App import db

def get_user_by_username(username):
    try:
        user = User.query.filter_by(username=username).first()
        return user
    except Exception as e:
        raise Exception(f"Database error: {str(e)}")

def get_user_by_email(email):
    try:
        user = User.query.filter_by(email=email).first()
        return user
    except Exception as e:
        raise Exception(f"Database error: {str(e)}")

def add_user(username, email, password):
    new_user = User(username=username, email=email, password=password)
    try:
        db.session.add(new_user)
        db.session.commit()
        return new_user
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Database error: {str(e)}")
