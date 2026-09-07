import os
from dotenv import load_dotenv
load_dotenv()  # Load .env file before Config reads env vars

from flask import Flask
from flask_login import LoginManager
from config import Config
from models import db
from models.user import User

def create_app(config_overrides=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if config_overrides:
        app.config.update(config_overrides)

    # Initialize Database
    db.init_app(app)

    # Initialize Login Manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'warning'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register Blueprints
    from routes import auth_bp, pages_bp, api_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(pages_bp)
    app.register_blueprint(api_bp)

    # Create tables
    with app.app_context():
        try:
            db.create_all()
            print("Database setup completed successfully.")
        except Exception as e:
            print(f"Error during database initialization: {e}")

    return app

# Instance execution
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)