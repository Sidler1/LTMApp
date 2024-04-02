# long_term_memory_app/app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    with app.app_context():
        db.init_app(app)
        migrate = Migrate(app, db)
        from .api import routes as api_routes
        app.register_blueprint(api_routes.api, url_prefix='/api')

    return app
