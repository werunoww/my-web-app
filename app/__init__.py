from flask import Flask
from .extensions import db, migrate, login_manager, assets
from .bundles import bundles, register_bundles
from .config import Config

from .routes.user import user
from .routes.apiary import apiary
from .routes.main import main

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    app.register_blueprint(main)
    app.register_blueprint(user)
    app.register_blueprint(apiary)
    
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    assets.init_app(app)
    
    # LOGIN MANAGER
    login_manager.login_view = 'user.login'
    login_manager.login_message = 'Для доступа к данной странице необходима авторизация'
    login_manager.login_message_category = "info"
    
    # ASSETS
    register_bundles(assets, bundles)
    
    with app.app_context():
        db.create_all()
        
    return app


