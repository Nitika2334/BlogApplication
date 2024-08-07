import os
import re
import datetime
import time
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt
from flask import request, current_app, jsonify
from .schema import (
    get_user_by_username, get_user_by_email, add_user, create_new_comment, 
    get_comments_by_post_id, update_existing_comment, delete_existing_comment,
    create_post as schema_create_post, get_post_by_id as schema_get_post_by_id, 
    update_post as schema_update_post, delete_post as schema_delete_post, 
    get_paginated_posts as schema_get_paginated_posts
)

from App.api.logger import info_logger,log_error,error_logger

REVOKED_TOKENS = {}

# Utility Functions

def validate_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email)

def validate_password(password):
    password_regex = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    return re.match(password_regex, password)

def user_register(data):
    try:
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            info_logger('user_register', 'Missing username, email, or password', username=username, email=email)
            return {
                'message': 'Please provide username, email, and password.',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40001'}
            }, 400

        if not validate_email(email):
            info_logger('user_register', 'Invalid email format', email=email)
            return {
                'message': 'Email format is invalid.',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40013'}
            }, 400

        if not validate_password(password):
            info_logger('user_register', 'Password does not meet criteria', username=username)
            return {
                'message': 'Password does not meet criteria.',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40011'}
            }, 400

        existing_user = get_user_by_username(username)
        if existing_user:
            info_logger('user_register', 'User already exists', username=username)
            return {
                'message': 'Username already exists.',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40002'}
            }, 400

        existing_email = get_user_by_email(email)
        if existing_email:
            info_logger('user_register', 'Email already exists', email=email)
            return {
                'message': 'Email already exists.',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40002'}
            }, 400

        hashed_password = generate_password_hash(password)
        new_user = add_user(username, email, hashed_password)

        expires = datetime.timedelta(minutes=30)
        access_token = create_access_token(identity=new_user.uid, expires_delta=expires)

        info_logger('user_register', 'User registered successfully', user_id=str(new_user.uid), username=username, email=email)
        
        return {
            'message': 'User registered successfully.',
            'status': True,
            'type': 'success_message',
            'error_status': {'error_code': '00000'},
            'data': {
                'user_id': str(new_user.uid),
                'access_token': access_token,
                'username': new_user.username,
                'email': new_user.email
            }
        }, 200
    except Exception as e:
        error_logger('user_register', 'Registration failed', error=str(e))
        return {
            'message': f'Registration failed: {str(e)}',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40000'}
        }, 400

def user_login(data):
    try:
        username = data.get('username')
        password = data.get('password')
        user = get_user_by_username(username)

        if user and check_password_hash(user.password, password):
            user_id = str(user.uid)
            expires = datetime.timedelta(minutes=120)
            access_token = create_access_token(identity=user.uid, expires_delta=expires)
            info_logger('user_login', 'User logged in successfully', user_id=user_id, username=username)
            return {
                'message': 'User logged in successfully',
                'status': True,
                'type': 'success_message',
                'error_status': {'error_code': '00000'},
                'data': {
                    'user_id': user_id,
                    'username': user.username,
                    'access_token': access_token
                }
            }, 200
        else:
            info_logger('user_login', 'Invalid credentials', username=username)
            return {
                'message': 'Invalid credentials',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40004'}
            }, 400
    except Exception as e:
        error_logger('user_login', 'Login failed', error=str(e))
        return {
            'message': f'Login failed: {str(e)}',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40000'}
        }, 400

def user_logout():
    try:
        jti = get_jwt()['jti']
        exp = get_jwt()['exp']  
        REVOKED_TOKENS[jti] = exp
        info_logger('user_logout', 'User logged out successfully', jti=jti)
        return {
            'message': 'User logged out successfully',
            'status': True,
            'type': 'success_message',
            'error_status': {'error_code': '00000'}
        }, 200
    except Exception as e:
        error_logger('user_logout', 'Logout failed', error=str(e))
        return {
            'message': f'Logout failed: {str(e)}',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40005'}
        }, 400

def is_token_revoked(jwt_payload):
    jti = jwt_payload['jti']
    now = time.time()
    for token, exp in list(REVOKED_TOKENS.items()):
        if exp < now:
            del REVOKED_TOKENS[token]

    return jti in REVOKED_TOKENS

# Comments

def comment_to_dict(comment):
    return {
        'uid': str(comment.uid),
        'content': comment.content,
        'user_uid': str(comment.user_uid),
        'post_uid': str(comment.post_uid),
        'created_at': comment.created_at.isoformat(),
        'updated_at': comment.updated_at.isoformat(),
    }


def create_comment(data, post_uid, user_uid):
    try:
        content = data.get('content')
        if not content:
            info_logger('create_comment', 'Content is required', post_uid=post_uid, user_uid=user_uid)
            return {
                'message': 'Content is required',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40012'}
            }, 400
        
        new_comment = create_new_comment(post_uid, user_uid, content)
        info_logger('create_comment', 'Comment created successfully', comment_id=new_comment.uid, post_uid=post_uid, user_uid=user_uid)
        return {
            'message': 'Comment created successfully',
            'status': True,
            'type': 'success_message',
            'error_status': {'error_code': '00000'},
            'data': {
                'comment_id': str(new_comment.uid),
                'post_id': str(post_uid),
                'user_id': str(user_uid),
                'content': new_comment.content,
                'created_at': str(new_comment.created_at)
            }
        }, 200
    except Exception as e:
        error_logger('create_comment', 'Failed to create comment', error=str(e))
        return {
            'message': f'Failed to create comment: {str(e)}',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40013'}
        }, 400
    
def get_comments(post_uid):
    try:
        comments = get_comments_by_post_id(post_uid)
        comments_list = [comment_to_dict(comment) for comment in comments]
        info_logger('get_comments', 'Comments retrieved successfully', post_uid=post_uid)
        return {
            'message': 'Comments retrieved successfully',
            'status': True,
            'type': 'success_message',
            'error_status': {'error_code': '00000'},
            'data': {
                'comments': comments_list
            }
        }, 200
    except Exception as e:
        error_logger('get_comments', 'Failed to get comments', error=str(e))
        return {
            'message': f'Failed to get comments: {str(e)}',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40014'}
        }, 400
    
def update_comment(data, comment_id, user_id):
    try:
        content = data.get('content')
        if not content:
            info_logger('update_comment', 'Content is required', comment_id=comment_id, user_id=user_id)
            return {
                'message': 'Content is required',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40012'}
            }, 400
        
        response_data, status_code = update_existing_comment(comment_id, content, user_id)
        info_logger('update_comment', 'Comment updated successfully', comment_id=comment_id, user_id=user_id)
        return response_data, status_code
    except Exception as e:
        error_logger('update_comment', 'Failed to update comment', error=str(e))
        return {
            'message': f'Failed to update comment: {str(e)}',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40016'}
        }, 400

def delete_comment(comment_id, user_id):
    try:
        response_data, status_code = delete_existing_comment(comment_id, user_id)
        info_logger('delete_comment', 'Comment deleted successfully', comment_id=comment_id, user_id=user_id)
        return response_data, status_code
    except Exception as e:
        error_logger('delete_comment', 'Failed to delete comment', error=str(e))
        return {
            'message': f'Failed to delete comment: {str(e)}',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40018'}
        }, 400


# Post

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

def create_new_post(data):
    try:
        title = data.get('title')
        content = data.get('content')
        image_file = request.files.get('image')

        if not title or not content:
            info_logger('create_new_post', 'Title and content are required')
            return {
                'message': 'Title and content are required',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40012'}
            }, 400

        image_url = None
        if image_file:
            image_url = save_image(image_file)

        new_post = schema_create_post(title, content, get_jwt_identity(), image_url)
        info_logger('create_new_post', 'Post created successfully', post_id=new_post.uid)
        return {
            'message': 'Post created successfully',
            'status': True,
            'type': 'success_message',
            'error_status': {'error_code': '00000'},
            'data': {
                'post_id': str(new_post.uid),
                'title': new_post.title,
                'content': new_post.content,
                'image_url': new_post.image
            }
        }, 200
    except Exception as e:
        error_logger('create_new_post', 'Error creating post', error=str(e))
        return {
            'message': f'Error creating post: {str(e)}',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40000'}
        }, 400
    
    
def save_image(image_file, old_filename=None):
    if not image_file or not allowed_file(image_file.filename):
        return None

    # Delete old image if it exists
    if old_filename:
        old_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], old_filename)
        if os.path.exists(old_image_path):
            os.remove(old_image_path)

    # Save the new image
    filename = secure_filename(image_file.filename)
    upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    image_file.save(upload_path)
    return filename

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png', 'gif'}

def get_post(post_id):
    try:
        post = schema_get_post_by_id(post_id)
        if not post:
            info_logger('get_post', 'Post not found', post_id=post_id)
            return {
                'message': 'Post not found',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40008'}
            }, 404
        if post:
            info_logger('get_post', 'Post retrieved successfully', post_id=post_id)
            return {
                'message': 'Post retrieved successfully',
                'status': True,
                'type': 'success_message',
                'error_status': {'error_code': '00000'},
                'data': post_to_dict(post)
            }, 200
    except Exception as e:
        error_logger('get_post', 'Error retrieving post', error=str(e))
        return {
            'message': f'Error retrieving post: {str(e)}',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40021'}
        }, 400

def update_post(post_id, data):
    try:
        title = data.get('title')
        content = data.get('content')
        image_file = request.files.get('image')
        user_id = get_jwt_identity()

        if not title and not content and not image_file:
            info_logger('update_post', 'Title, content, or image is required.', post_id=post_id, user_id=user_id)
            return {
                'message': 'Title, content, or image is required.',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40007'}
            }, 400

        post = schema_get_post_by_id(post_id)
        if not post:
            info_logger('update_post', 'Post not found', post_id=post_id)
            return {
                'message': 'Post not found',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40008'}
            }, 404

        if str(post.user_uid) != user_id:
            info_logger('update_post', 'Unauthorized update attempt', post_id=post_id, user_id=user_id)
            return {
                'message': 'You are not authorized to update this post.',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40006'}
            }, 400

        # Handle updating image
        if image_file:
            old_image_url = post.image
            image_url = save_image(image_file, old_image_url)
            success = schema_update_post(post_id, title, content, image_url)
        else:
            success = schema_update_post(post_id, title, content)

        if success:
            info_logger('update_post', 'Post updated successfully', post_id=post_id)
            return {
                'message': 'Post updated successfully.',
                'status': True,
                'type': 'success_message',
                'error_status': {'error_code': '00000'}
            }, 200
        else:
            return {
                'message': 'Failed to update post.',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40009'}
            }, 400
    except Exception as e:
        error_logger('update_post', 'Failed to update post', error=str(e))
        return {
            'message': f'Failed to update post: {str(e)}',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40009'}
        }, 400



def delete_post(post_id, user_id):
    try:
        post = schema_get_post_by_id(post_id)
        if not post:
            info_logger('delete_post', 'Post not found', post_id=post_id)
            return {
                'message': 'Post not found',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40008'}
            }, 404

        if str(post.user_uid) != user_id:
            info_logger('delete_post', 'Unauthorized delete attempt', post_id=post_id, user_id=user_id)
            return {
                'message': 'You are not authorized to delete this post.',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40006'}
            }, 400

        old_image_url = post.image
        success = schema_delete_post(post_id, user_id)

        if success:
            # Delete the image file
            if old_image_url:
                image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], old_image_url)
                if os.path.exists(image_path):
                    os.remove(image_path)
            info_logger('delete_post', 'Post deleted successfully', post_id=post_id)
            return {
                'message': 'Post deleted successfully.',
                'status': True,
                'type': 'success_message',
                'error_status': {'error_code': '00000'}
            }, 200
        else:
            return {
                'message': 'Failed to delete post.',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40010'}
            }, 400
    except Exception as e:
        error_logger('delete_post', 'Failed to delete post', error=str(e))
        return {
            'message': f'Failed to delete post: {str(e)}',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40011'}
        }, 400

def get_posts(page, per_page, user_uid=None):
    try:
        posts, total_posts = schema_get_paginated_posts(page, per_page, user_uid)
        posts_list = [post_to_dict(post) for post in posts]
        info_logger('get_posts', 'Posts retrieved successfully', page=page, per_page=per_page, user_uid=user_uid)
        return {
            'message': 'Posts retrieved successfully',
            'status': True,
            'type': 'success_message',
            'error_status': {'error_code': '00000'},
            'data': {
                'posts': posts_list
            }
        }, 200
    except Exception as e:
        error_logger('get_posts', 'Error retrieving posts', error=str(e))
        return {
            'message': f'Error retrieving posts: {str(e)}',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40024'}
        }, 400

def get_home_page_data(page, size, user_id=None):
    try:
        # Validate the page and size parameters
        page = int(page)
        size = int(size)
        if page < 1 or size < 1:
            raise ValueError("Page and size must be positive integers.")

        # Retrieve paginated posts
        posts, total_posts = schema_get_paginated_posts(page, size, user_uid=user_id)

        data = {
            "current_page": page,
            "page_size": size,
            "total_pages": (total_posts + size - 1) // size,
            "total_posts": total_posts,
            "posts": [post_to_dict(post) for post in posts]
        }

        info_logger('get_home_page_data', 'Home page data retrieved successfully', page=page, size=size, user_id=user_id)
        
        return {
            'message': 'Home page data retrieved successfully.',
            'status': True,
            'type': 'success_message',
            'error_status': {'error_code': '00000'},
            'data': data
        }, 200
    except ValueError as ve:
        error_logger('get_home_page_data', 'Invalid pagination parameters', error=str(ve), page=page, size=size, user_id=user_id)
        return {
            'message': f'Invalid pagination parameters: {str(ve)}',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40016'}
        }, 400
    except Exception as e:
        # Log general errors
        error_logger('get_home_page_data', 'Failed to retrieve home page data', error=str(e), page=page, size=size, user_id=user_id)
        return {
            'message': f'Failed to retrieve home page data: {str(e)}',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40016'}
        }, 400

