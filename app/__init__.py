from flask import Flask
from app.db.database import init_db
from app.views.item_views import item_bp


def create_app():
    app = Flask(__name__)

    app.config.from_object('config.Config')

    # Initialize database
    init_db(app)

    # Register blueprints
    app.register_blueprint(item_bp, url_prefix='/items')

    return app
