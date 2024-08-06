from App.Models.User.UserModel import User
from App.Models.Comment.CommentModel import Comment
from App import db

def get_user_by_username(username):
    try:
        user = User.query.filter_by(username=username).first()
        return user
    except Exception:
        raise Exception("Database error")

def get_user_by_email(email):
    try:
        user = User.query.filter_by(email=email).first()
        return user
    except Exception:
        raise Exception("Database error")

def add_user(username, email, password):
    try:
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return new_user
    except Exception:
        db.session.rollback()
        raise Exception("Database error")
    

#Comments    

def get_comments_by_post_id(post_uid):
    try:
        comments = Comment.query.filter_by(post_uid=post_uid).all()
        return comments
    except Exception:
        raise Exception("Database error")

def create_new_comment(post_uid, user_uid, content):
    try:  
        new_comment = Comment(content=content, user_uid=user_uid, post_uid=post_uid)
        db.session.add(new_comment)
        db.session.commit()
        return new_comment
    except Exception:
        db.session.rollback()
        raise Exception("Database error")

def update_existing_comment(comment_id, content):
    try:
        comment = Comment.query.filter_by(uid=comment_id).first()
        if comment:
            comment.content = content
            db.session.commit()
            return True
        else:
            return False
    except Exception:
        db.session.rollback()
        raise Exception("Database error")

def delete_existing_comment(comment_id, user_uid):
    try:
        comment = Comment.query.filter_by(uid=comment_id, user_uid=user_uid).first()
        if comment:
            db.session.delete(comment)
            db.session.commit()
            return True
        else:
            return False
    except Exception:
        db.session.rollback()
        raise Exception("Database error")
