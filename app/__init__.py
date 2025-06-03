from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from instance.config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))

    from app.routes import bp
    app.register_blueprint(bp)

    with app.app_context():
        from app.models import User, Documentation
        db.create_all()

    return app
