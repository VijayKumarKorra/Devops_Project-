from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config_object=None):
    app = Flask(__name__)

    if config_object is None:
        from userapi.src.config import Config
        app.config.from_object(Config)
    else:
        app.config.from_object(config_object)

    db.init_app(app)

    with app.app_context():
        from userapi.src import routes
        app.register_blueprint(routes.bp)
        db.create_all()

    return app
