from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os

# 1. Import the EXISTING database instance from your models file!
from app.models import db 

# 2. Globally initialize the other extensions
login_manager = LoginManager()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    
    # Load configuration from config.py
    app.config.from_object('config.Config')

    # 3. Bind all extensions to the main app
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    # Configure Login Manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'danger'

    # 4. Register Blueprints (Imported here to avoid circular imports)
    from app.routes import main
    from app.auth import auth 
    
    app.register_blueprint(main)
    app.register_blueprint(auth)

    # 5. User Loader for Flask-Login
    from app.models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app