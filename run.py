#!/usr/bin/env python3
"""
Flask-OpenAI GPT Clone Application
Run this file to start the web server.
"""
import os
from dotenv import load_dotenv
from app import create_app

# Load environment variables from .env file
load_dotenv()

# Create the Flask application
app = create_app()

if __name__ == '__main__':
    # Get configuration from environment variables
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    print("🚀 Starting GPT Clone server...")
    print(f"📱 Visit: http://{host}:{port}")
    print(f"🔧 Debug mode: {debug}")
    
    # Run the application
    app.run(host=host, port=port, debug=debug)
