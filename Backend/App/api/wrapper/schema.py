from App.Models.User.UserModel import User
from App.Models.Comment.CommentModel import Comment
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
    try:
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return new_user
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Database error: {str(e)}")
    

#Comments    

def get_comments_by_post_id(post_uid):
    try:
        comments = Comment.query.filter_by(post_uid=post_uid).all()
        return comments
    except Exception as e:
        raise Exception(f"Database error: {str(e)}")

def create_new_comment(post_uid, user_uid, content):
    try:  
        new_comment = Comment(content=content, user_uid=user_uid, post_uid=post_uid)
        db.session.add(new_comment)
        db.session.commit()
        return new_comment
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Database error: {str(e)}")

def update_existing_comment(comment_id, data, user_uid):
    try:
        comment = Comment.query.filter_by(uid=comment_id).first()
        if not comment:
            return {
                'message': 'Comment not found.',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40014'}
            }, 400

        if str(comment.user_uid) != user_uid:
            return {
                'message': 'You are not authorized to update this comment.',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40017'}
            }, 400

        comment.content = data.get('content', comment.content)
        db.session.commit()
        return {
            'message': 'Comment updated successfully.',
            'status': True,
            'type': 'success_message',
            'error_status': {'error_code': '00000'}
        }, 200
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Database error: {str(e)}") 

def delete_existing_comment(comment_id, user_uid):
    try:
        comment = Comment.query.filter_by(uid=comment_id).first()
        if not comment:
            return {
                'message': 'Comment not found.',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40014'}
            }, 400

        if str(comment.user_uid) != user_uid:
            return {
                'message': 'You are not authorized to delete this comment.',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40017'}
            }, 400

        db.session.delete(comment)
        db.session.commit()
        return {
            'message': 'Comment deleted successfully.',
            'status': True,
            'type': 'success_message',
            'error_status': {'error_code': '00000'}
        }, 200
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Database error: {str(e)}") 
