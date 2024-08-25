import os

class Config:

    SECRET_KEY = os.getenv('SECRET_KEY') or 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or 'postgresql+psycopg2://postgres:1525@localhost:5432/Blog_app'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY') or 'your_jwt_secret_key'
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

    @staticmethod
    def init_app(app):
        # Initialize other settings if needed
        Config.create_upload_folder(app.config['UPLOAD_FOLDER'])

    @staticmethod
    def create_upload_folder(path):
        # Create the uploads folder if it doesn't exist
        if not os.path.exists(path):
            try:
                os.makedirs(path)
                print(f"Created uploads folder at {path}")
            except Exception as e:
                print(f"Failed to create uploads folder: {str(e)}")
