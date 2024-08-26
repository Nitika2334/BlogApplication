import os

class Config:

    SECRET_KEY = os.getenv('SECRET_KEY') or 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or 'postgresql+psycopg2://postgres:1234@localhost:5432/Blog_app'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY') or 'your_jwt_secret_key'

    # Cloudinary Configuration
    CLOUD_NAME = os.getenv('CLOUD_NAME') or 'dhhnvmoz0'
    CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY') or '375616383349864'
    CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET') or 'Ov1DwK6OuGQ8grbL5xA4bd6AZV0'


    @staticmethod
    def create_upload_folder(path):
        # Create the uploads folder if it doesn't exist
        if not os.path.exists(path):
            try:
                os.makedirs(path)
                print(f"Created uploads folder at {path}")
            except Exception as e:
                print(f"Failed to create uploads folder: {str(e)}")

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:1234@localhost:5432/Blog_app'
    TESTING = True
    SECRET_KEY = 'your_secret_key'
    JWT_SECRET_KEY = 'your_jwt_secret_key'