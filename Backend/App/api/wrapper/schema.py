from sqlalchemy import desc
from App.Models.User.UserModel import User
from App.Models.Post.PostModel import Post
from App.Models.Comment.CommentModel import Comment
from App import db
from App.api.logger import info_logger, error_logger  # Import logging functions


def get_user_by_username(username):
    try:
        user = User.query.filter_by(username=username).first()
        info_logger('get_user_by_username', 'User retrieved successfully', username=username)
        return user
    except Exception as e:
        error_logger('get_user_by_username', 'Failed to retrieve user', error=str(e), username=username)
        raise Exception(f"Database error: {str(e)}")

def get_user_by_email(email):
    try:
        user = User.query.filter_by(email=email).first()
        info_logger('get_user_by_email', 'User retrieved successfully', email=email)
        return user
    except Exception as e:
        error_logger('get_user_by_email', 'Failed to retrieve user', error=str(e), email=email)
        raise Exception(f"Database error: {str(e)}")

def add_user(username, email, password):
    try:
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        info_logger('add_user', 'User added successfully', username=username, email=email)
        return new_user
    except Exception as e:
        db.session.rollback()
        error_logger('add_user', 'Failed to add user', error=str(e), username=username, email=email)
        raise Exception(f"Database error: {str(e)}")

# Post Functions

def create_post(title, content, user_uid, image=None):
    try:
        new_post = Post(title=title, content=content, user_uid=user_uid, image=image)
        db.session.add(new_post)
        db.session.commit()
        info_logger('create_post', 'Post created successfully', post_id=str(new_post.uid), user_uid=user_uid)
        return new_post
    except Exception as e:
        db.session.rollback()
        error_logger('create_post', 'Failed to create post', error=str(e), title=title, content=content)
        raise Exception(f"Database error: {str(e)}")

def update_post(post_id, title, content, image=None):
    try:
        post = Post.query.filter_by(uid=post_id).first()
        if not post:
            error_logger('update_post', 'Post not found', post_id=post_id)
            return False

        if title:
            post.title = title
        if content:
            post.content = content
        if image is not None:
            post.image = image

        db.session.commit()
        info_logger('update_post', 'Post updated successfully', post_id=post_id)
        return True
    except Exception as e:
        db.session.rollback()
        error_logger('update_post', 'Failed to update post', error=str(e), post_id=post_id)
        raise Exception(f"Database error: {str(e)}")

def get_post_by_id(post_id):
    try:
        post = Post.query.filter_by(uid=post_id).first()
        if post:
            info_logger('get_post_by_id', 'Post retrieved successfully', post_id=post_id)
            return post
        else:
            error_logger('get_post_by_id', 'Post not found', post_id=post_id)
            return None
    except Exception as e:
        error_logger('get_post_by_id', 'Failed to retrieve post', error=str(e), post_id=post_id)
        raise Exception(f"Database error: {str(e)}")

def save_image(image_file, filename):
    try:
        image_path = f"App/api/uploads/{filename}"
        image_file.save(image_path)
        info_logger('save_image', 'Image saved successfully', filename=filename)
        return filename
    except Exception as e:
        error_logger('save_image', 'Failed to save image', error=str(e), filename=filename)
        raise Exception(f"Database error: {str(e)}")

def post_to_dict(post):
    return {
        'uid': str(post.uid),
        'title': post.title,
        'content': post.content,
        'user_uid': str(post.user_uid),
        'created_at': post.created_at.isoformat(),
        'updated_at': post.updated_at.isoformat(),
        'image': post.image
    }

# def get_post(post_id):
#     try:
#         post = get_post_by_id(post_id)
#         if post:
#             return {
#                 'message': 'Post retrieved successfully',
#                 'status': True,
#                 'type': 'success_message',
#                 'error_status': {'error_code': '00000'},
#                 'data': post_to_dict(post)
#             }, 200
#         else:
#             return {
#                 'message': 'Post not found',
#                 'status': False,
#                 'type': 'custom_error',
#                 'error_status': {'error_code': '40019'}
#             }, 404
#     except Exception as e:
#         return {
#             'message': f'Error retrieving post: {str(e)}',
#             'status': False,
#             'type': 'custom_error',
#             'error_status': {'error_code': '40021'}
#         }, 400

def delete_post(post_id, user_uid):
    try:
        post = Post.query.filter_by(uid=post_id).first()
        if not post:
            return {
                'message': 'Post not found',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40019'}
            }, 404

        if str(post.user_uid) != user_uid:
            return {
                'message': 'Unauthorized action',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40022'}
            }, 403

        db.session.delete(post)
        db.session.commit()
        info_logger('delete_post', 'Post deleted successfully', post_id=post_id)
        return {
            'message': 'Post deleted successfully',
            'status': True,
            'type': 'success_message',
            'error_status': {'error_code': '00000'}
        }, 200
    except Exception as e:
        db.session.rollback()
        error_logger('delete_post', 'Failed to delete post', error=str(e), post_id=post_id)
        raise Exception(f"Database error: {str(e)}")

# Comment Functions

def get_comments_by_post_id(post_uid):
    try:
        comments = Comment.query.filter_by(post_uid=post_uid).all()
        info_logger('get_comments_by_post_id', 'Comments retrieved successfully', post_uid=post_uid)
        return comments
    except Exception as e:
        error_logger('get_comments_by_post_id', 'Failed to retrieve comments', error=str(e), post_uid=post_uid)
        raise Exception(f"Database error: {str(e)}")

def create_new_comment(post_uid, user_uid, content):
    try:
        new_comment = Comment(content=content, user_uid=user_uid, post_uid=post_uid)
        db.session.add(new_comment)
        db.session.commit()
        info_logger('create_new_comment', 'Comment created successfully', post_uid=post_uid, user_uid=user_uid)
        return new_comment
    except Exception as e:
        db.session.rollback()
        error_logger('create_new_comment', 'Failed to create comment', error=str(e), post_uid=post_uid, user_uid=user_uid, content=content)
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
        info_logger('update_existing_comment', 'Comment updated successfully', comment_id=comment_id)
        return {
            'message': 'Comment updated successfully.',
            'status': True,
            'type': 'success_message',
            'error_status': {'error_code': '00000'}
        }, 200
    except Exception as e:
        db.session.rollback()
        error_logger('update_existing_comment', 'Failed to update comment', error=str(e), comment_id=comment_id)
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
        info_logger('delete_existing_comment', 'Comment deleted successfully', comment_id=comment_id)
        return {
            'message': 'Comment deleted successfully.',
            'status': True,
            'type': 'success_message',
            'error_status': {'error_code': '00000'}
        }, 200
    except Exception as e:
        db.session.rollback()
        error_logger('delete_existing_comment', 'Failed to delete comment', error=str(e), comment_id=comment_id)
        raise Exception(f"Database error: {str(e)}")


def get_paginated_posts(page, per_page, user_uid=None):
    try:
        page = int(page)
        per_page = int(per_page)
        if page < 1 or per_page < 1:
            raise ValueError("Page and per_page must be positive integers.")

        offset = (page - 1) * per_page

        query = db.session.query(Post).order_by(desc(Post.created_at))

        if user_uid:
            query = query.filter(Post.user_uid == user_uid)

        total_posts = query.count()

        posts = query.offset(offset).limit(per_page).all()

        info_logger('get_paginated_posts', 'Posts retrieved successfully', page=page, per_page=per_page, user_uid=user_uid)
        
        return posts, total_posts
    except ValueError as ve:
        error_logger('get_paginated_posts', 'Invalid pagination parameters', error=str(ve), page=page, per_page=per_page, user_uid=user_uid)
        raise ValueError(f"Invalid pagination parameters: {str(ve)}")
    except Exception as e:
        error_logger('get_paginated_posts', 'Failed to retrieve posts', error=str(e), page=page, per_page=per_page, user_uid=user_uid)
        raise Exception(f"Database error: {str(e)}")
