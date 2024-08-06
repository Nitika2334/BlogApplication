from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from App.config import Config
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        from App.api.wrapper.utils import is_token_revoked
        return is_token_revoked(jwt_payload)

    from App.Models.User.UserModel import User
    from App.Models.Comment.CommentModel import Comment
    from App.Models.Post.PostModel import Post

    with app.app_context():
        db.create_all() 
    

    from App.api.route import route
    app.register_blueprint(route,url_prefix='/api/v1')
    return app
