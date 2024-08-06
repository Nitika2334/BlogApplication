from App.Models.User.UserModel import User
from App.Models.Post.PostModel import Post
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

def get_post_by_id(post_id):
    try:
        post = Post.query.filter_by(id=post_id).first()
        return post
    except Exception as e:
        raise Exception(f"Database error: {str(e)}")

def create_post(title, content, author_id):
    new_post = Post(title=title, content=content, author_id=author_id)
    try:
        db.session.add(new_post)
        db.session.commit()
        return new_post
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Database error: {str(e)}")

def update_post(post_id, title, content):
    try:
        post = Post.query.filter_by(id=post_id).first()
        if post:
            post.title = title
            post.content = content
            db.session.commit()
            return post
        else:
            raise Exception("Post not found")
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Database error: {str(e)}")

def delete_post(post_id):
    try:
        post = Post.query.filter_by(id=post_id).first()
        if post:
            db.session.delete(post)
            db.session.commit()
            return post
        else:
            raise Exception("Post not found")
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Database error: {str(e)}")
