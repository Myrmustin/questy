"Has our application"
from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from config import DevConfig
from models import Recipe, User
from exts import db
from flask_migrate import Migrate 
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required
from recipes import recipe_ns
from auth import auth_ns

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    JWTManager(app)
    api = Api(app, doc = '/docs')
    api.add_namespace(recipe_ns)
    api.add_namespace(auth_ns)
    migrate = Migrate(app,db)

    @app.shell_context_processor
    def make_shell_context():
        return {
            "db" : db,
            "Recipe": Recipe,
            "User": User
        }

    return app

