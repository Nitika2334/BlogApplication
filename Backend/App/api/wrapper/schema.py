from App.Models.User.UserModel import User
from App.Models.Post.PostModel import Post
from App import db

# User-related functions
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

# Post Functions

def create_new_post(title, content, user_uid):
    try:
        new_post = Post(title=title, content=content, user_uid=user_uid)
        db.session.add(new_post)
        db.session.commit()
        return new_post
    except Exception:
        db.session.rollback()
        raise Exception("Database error")

def get_post_by_id(post_id):
    try:
        post = Post.query.filter_by(uid=post_id).first()
        return post
    except Exception:
        raise Exception("Database error")

def update_post(post_id, title, content):
    try:
        post = Post.query.filter_by(uid=post_id).first()
        if post:
            if title:
                post.title = title
            if content:
                post.content = content
            db.session.commit()
            return True
        else:
            return False
    except Exception:
        db.session.rollback()
        raise Exception("Database error")

def delete_post(post_id, user_uid):
    try:
        post = Post.query.filter_by(uid=post_id, user_uid=user_uid).first()
        if post:
            db.session.delete(post)
            db.session.commit()
            return True
        else:
            return False
    except Exception:
        db.session.rollback()
        raise Exception("Database error")