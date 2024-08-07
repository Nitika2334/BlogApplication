from sqlalchemy import desc
from App.Models.User.UserModel import User
from App.Models.Post.PostModel import Post
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


# Posts
def create_post(title, content, user_uid, image=None):
    try:
        new_post = Post(title=title, content=content, user_uid=user_uid, image=image)
        db.session.add(new_post)
        db.session.commit()
        return new_post
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Database error: {str(e)}")


def update_post(post_id, title, content, image=None):
    try:
        post = Post.query.filter_by(uid=post_id).first()
        if post:
            if title:
                post.title = title
            if content:
                post.content = content
            if image is not None:
                post.image = image
            db.session.commit()
            return True
        else:
            return False
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Database error: {str(e)}")



def get_post_by_id(post_id):
    try:
        return Post.query.filter_by(uid=post_id).first()
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Database error: {str(e)}")

def save_image(image_file, filename):
    try:
        image_path = f"App/api/uploads/{filename}"
        image_file.save(image_path)
        return filename
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Database error: {str(e)}")

def post_to_dict(post):
    return {
        'uid': str(post.uid),
        'title': post.title,
        'content': post.content,
        'user_uid': str(post.user_uid),
        'created_at': post.created_at.isoformat(),
        'updated_at': post.updated_at.isoformat(),
        'image': post.image  # Correct field name
    }

def get_post(post_id):
    try:
        post = get_post_by_id(post_id)
        return {
            'message': 'Post retrieved successfully',
            'status': True,
            'type': 'success_message',
            'error_status': {'error_code': '00000'},
            'data': post_to_dict(post)
        }, 200
    except Exception as e:
        return {
            'message': f'Error retrieving post: {str(e)}',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40021'}
        }, 400



def delete_post(post_id, user_uid):
    try:
        post = Post.query.filter_by(uid=post_id).first()
        if not post:
            return False

        if str(post.user_uid) != user_uid:
            return False

        db.session.delete(post)
        db.session.commit()
        return True
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

def update_existing_comment(comment_id, user_uid, updated_data):
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

        comment.content = updated_data.get('content', comment.content)
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


def get_paginated_posts(page, per_page, user_uid=None):
    query = db.session.query(Post).order_by(desc(Post.created_at))  # Sort by creation date in descending order

    if user_uid:
        query = query.filter(Post.user_uid == user_uid)

    total_posts = query.count()
    posts = query.offset((page - 1) * per_page).limit(per_page).all()

    return posts, total_posts


