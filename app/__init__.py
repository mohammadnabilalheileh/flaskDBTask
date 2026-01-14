from flask import Flask
from .config import Config
from .extensions import db, migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes.libraries import libraries_bp
    from app.routes.books import books_bp
    from app.routes.users import users_bp

    app.register_blueprint(libraries_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(users_bp)

    return app
