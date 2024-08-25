import os
import re
import datetime
import time
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt
from flask import request, jsonify
from .schema import (
    get_user_by_username, get_user_by_email, add_user, create_new_comment, 
    get_comments_by_post_id, update_existing_comment, delete_existing_comment, get_comment_by_comment_id,
    create_post_db , get_post_by_id, update_post_db, delete_post_db, get_paginated_posts_db, get_user_by_user_id,get_comment_count_for_post
)

from App.config import Config
from App.api.logger import error_logger

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
            return {
                'message': 'Please provide username, email, and password.',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40001'}
            }, 400

        if not validate_email(email):
            return {
                'message': 'Email format is invalid.',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40013'}
            }, 400

        if not validate_password(password):
            return {
                'message': 'Password does not meet criteria.',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40011'}
            }, 400
        existing_user = get_user_by_username(username)
        if existing_user:
            return {
                'message': 'Username already exists.',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40002'}
            }, 400

        existing_email = get_user_by_email(email)
        if existing_email:
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
            'message': 'Registration failed',
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
            expires = datetime.timedelta(minutes=30)
            access_token = create_access_token(identity=user.uid, expires_delta=expires)
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
            return {
                'message': 'Invalid credentials',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40004'}
            }, 400
    except Exception as e:
        error_logger('user_login', 'Login failed', error=str(e))
        return {
            'message': 'Login failed',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40000'}
        }, 400

def user_logout():
    try:
        jti = get_jwt()['jti']
        exp = get_jwt()['exp']  
        REVOKED_TOKENS[jti] = exp
        return {
            'message': 'User logged out successfully',
            'status': True,
            'type': 'success_message',
            'error_status': {'error_code': '00000'}
        }, 200
    except Exception as e:
        error_logger('user_logout', 'Logout failed', error=str(e))
        return {
            'message': 'Logout failed',
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
        'username':comment.username,
        'created_at': comment.created_at.isoformat(),
        'updated_at': comment.updated_at.isoformat(),
    }


def create_comment(data, post_uid, user_uid):
    try:
        user=get_user_by_user_id(user_uid)
        new_comment = create_new_comment(post_uid, user_uid, data, user.username)
        if new_comment:
            return {
            'message': 'Comment created successfully',
            'status': True,
            'type': 'success_message',
            'error_status': {'error_code': '00000'},
            'data': {
                'comment_id': str(new_comment.uid),
                'post_id': str(post_uid),
                'username':user.username,
                'user_id': str(user_uid),
                'content': new_comment.content,
                'created_at': str(new_comment.created_at)
            }
        }, 200
    except Exception as e:
        error_logger('create_comment', 'Failed to create comment', error=str(e))
        return {
            'message': 'Failed to create comment',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40013'}
        }, 400
    
def get_comments(post_uid):
    try:
        comments = get_comments_by_post_id(post_uid)
        comments_list = [comment_to_dict(comment) for comment in comments]
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
            'message': 'Failed to get comments',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40014'}
        }, 400
    
def update_comment(data, comment_id, user_id):
    try:
        comment=get_comment_by_comment_id(comment_id)
        if not comment:
            return {
                'message': 'Comment not found.',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40014'}
            }, 400
        
        if str(comment.user_uid) != user_id:
            return {
                'message': 'You are not authorized to update this comment.',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40017'}
            }, 400
        sucess= update_existing_comment(comment,data)

        if sucess:
            return {
            'message': 'Comment updated successfully.',
            'status': True,
            'type': 'success_message',
            'error_status': {'error_code': '00000'}
        }, 200
        else:
            return{
            'message': 'Comment not Updated',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40013'}
            }, 400
    except Exception as e:
        error_logger('update_comment', 'Failed to update comment', error=str(e), comment_id=comment_id)
        return {
            'message': 'Failed to update comment',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40016'}
        }, 400

def delete_comment(comment_id, user_id):
    try:
        comment=get_comment_by_comment_id(comment_id)
        if not comment:
            return {
                'message': 'Comment not found.',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40014'}
            }, 400
        
        if str(comment.user_uid) != user_id:
            return {
                'message': 'You are not authorized to delete this comment.',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40017'}
            }, 400
        success = delete_existing_comment(comment)
        if success:
             return {
            'message': 'Comment deleted successfully.',
            'status': True,
            'type': 'success_message',
            'error_status': {'error_code': '00000'}
        }, 200
        else:
            return{
            'message': 'Comment not Deleted',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40013'}
            },400
    except Exception as e:
        error_logger('delete_comment', 'Failed to delete comment', error=str(e), comment_id=comment_id)
        return {
            'message': 'Failed to delete comment',
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
        'username':post.username,
        'created_at': post.created_at.isoformat(),
        'updated_at': post.updated_at.isoformat(),
        'image': post.image,
        'no_of_comments' : get_comment_count_for_post(post.uid)
    }

from werkzeug.utils import secure_filename
import os
import base64
from io import BytesIO
from PIL import Image
import uuid

def create_new_post(data):
    try:
        if data.content_type == 'application/json':
            json_data = data.get_json()
            title = json_data.get('title')
            content = json_data.get('content')
            image_base64 = json_data.get('image')  
        else:
            title = data.form.get('title')
            content = data.form.get('content')
            image_file = data.files.get('image')

        if not title or not content:
            return {
                'message': 'Title and content are required',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40012'}
            }, 400

        image_url = None
        if image_file:
            image_url = save_image(image_file)
        elif image_base64:
            image_url = save_image_from_base64(image_base64)

        user = get_user_by_user_id(get_jwt_identity())
        new_post = create_post_db(title, content, get_jwt_identity(), user.username, image_url)
        
        return {
            'message': 'Post created successfully',
            'status': True,
            'type': 'success_message',
            'error_status': {'error_code': '00000'},
            'data': {
                'post_id': str(new_post.uid),
                'title': new_post.title,
                'username': user.username,
                'content': new_post.content,
                'image_url': new_post.image
            }
        }, 200
    except Exception as e:
        error_logger('create_new_post', 'Error creating post', error=str(e))
        return {
            'message': 'Error creating post',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40000'}
        }, 400

def save_image(image_file, current_image_url=None):
    try:
        if image_file:
            filename = secure_filename(image_file.filename)
            file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
            image_file.save(file_path)
            
            if current_image_url and os.path.exists(current_image_url):
                os.remove(current_image_url)

            return file_path
        return current_image_url
    except Exception as e:
        error_logger('save_image', 'Failed to save image', error=str(e))
        return None

def save_image_from_base64(image_base64, current_image_url=None):
    try:
        if image_base64:
            image_data = base64.b64decode(image_base64)
            image = Image.open(BytesIO(image_data))
            filename = secure_filename(f'image_{str(uuid.uuid4())}.png')
            file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
            image.save(file_path)

            if current_image_url and os.path.exists(current_image_url):
                os.remove(current_image_url)

            return file_path
        return current_image_url
    except Exception as e:
        error_logger('save_image_from_base64', 'Failed to save image from Base64', error=str(e))
        return None

        

def get_post(post_id):
    try:
        post = get_post_by_id(post_id)
        if not post:
            return {
                'message': 'Post not found',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40008'}
            }, 400
        if post:
            return {
                'message': 'Post retrieved successfully',
                'status': True,
                'type': 'success_message',
                'error_status': {'error_code': '00000'},
                'data': post_to_dict(post)
            }, 200
    except Exception as e:
        print(str(e))
        error_logger('get_post', 'Error retrieving post', error=str(e))
        return {
            'message': 'Error retrieving post',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40021'}
        }, 400

def update_post(post_id, data):
    try:
        post = get_post_by_id(post_id)
        if not post:
            return {
                'message': 'Post not found.',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40022'}
            }, 400

        if data.content_type == 'application/json':
            json_data = data.get_json()
            title = json_data.get('title')
            content = json_data.get('content')
            new_image_base64 = json_data.get('image')  # Assume image is a Base64 string
        else:
            title = data.form.get('title')
            content = data.form.get('content')
            new_image_file = data.files.get('image')

        if title:
            post.title = title
        if content:
            post.content = content

        if new_image_file:
            new_image_url = save_image(new_image_file, post.image_url)
            post.image_url = new_image_url
        elif new_image_base64:
            new_image_url = save_image_from_base64(new_image_base64, post.image_url)
            post.image_url = new_image_url

        success = update_post_db(post)
        if success:
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
            'message': 'Failed to update post',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40009'}
        }, 400


def delete_post(post_id, user_id):
    try:
        post = get_post_by_id(post_id)
        if not post:
            return {
                'message': 'Post not found',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40008'}
            }, 400

        if str(post.user_uid) != user_id:
            return {
                'message': 'You are not authorized to delete this post.',
                'status': False,
                'type': 'custom_error',
                'error_status': {'error_code': '40006'}
            }, 400

        if post.image_url and os.path.exists(post.image_url):
            os.remove(post.image_url)
        success = delete_post_db(post_id, user_id)

        if success:
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
            'message': 'Failed to delete post',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40011'}
        }, 400

def get_home_page_data(page, size, user_id=None):
    try:
        # Validate the page and size parameters
        page = int(page)
        size = int(size)

        # Retrieve paginated posts
        posts, total_posts = get_paginated_posts_db(page, size, user_uid=user_id)

        data = {
            "current_page": page,
            "page_size": size,
            "total_pages": (total_posts + size - 1) // size,
            "total_posts": total_posts,
            "posts": [post_to_dict(post) for post in posts]
        }

        
        return {
            'message': 'Home page data retrieved successfully.',
            'status': True,
            'type': 'success_message',
            'error_status': {'error_code': '00000'},
            'data': data
        }, 200
    except Exception as e:
        # Log general errors
        error_logger('get_home_page_data', 'Failed to retrieve home page data', error=str(e), page=page, size=size, user_id=user_id)
        return {
            'message': 'Failed to retrieve home page data',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40016'}
        }, 400

