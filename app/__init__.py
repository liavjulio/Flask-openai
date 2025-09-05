import logging
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from openai import OpenAI
import os

db = SQLAlchemy()
openai_client = None

def create_app():
    global openai_client

    app = Flask(__name__, 
                static_folder='static',
                template_folder='templates')
    app.config.from_object('app.config.Config')

    logging.basicConfig(level=logging.DEBUG)
    app.logger.setLevel(logging.DEBUG)

    app.logger.debug("Initializing database")
    db.init_app(app)
    CORS(app)  # Initialize CORS for the entire app

    # Load SQLALCHEMY_DATABASE_URI from environment variable
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

    openai_api_key = app.config.get('OPENAI_API_KEY')
    if openai_api_key:
        app.logger.debug("Initializing OpenAI client")
        openai_client = OpenAI(api_key=openai_api_key)
    else:
        app.logger.error("OPENAI_API_KEY is not set in configuration")
        raise ValueError("OPENAI_API_KEY is not set in configuration")

    with app.app_context():
        app.logger.debug("Creating all tables")
        from .models import QnA, Conversation, Message
        db.create_all()
        app.logger.debug("All tables created")
    
    # Import routes and register blueprints
    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    app.logger.debug("App initialization complete")

    return app
