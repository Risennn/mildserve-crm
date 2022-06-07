import os
from flask import Flask

from .blueprints.api.cars_api import cars_api_bp
from .blueprints.api.dealers_api import dealers_api_bp
from .blueprints.general.general import general_bp
from .blueprints.dealers.dealers import dealers_bp
from .blueprints.cars.cars import cars_bp
from .extensions import db

basedir = os.path.abspath(os.path.dirname(__file__))


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    app.register_blueprint(dealers_api_bp, url_prefix="/api/v1/")
    app.register_blueprint(cars_api_bp, url_prefix="/api/v1/")
    app.register_blueprint(general_bp)
    app.register_blueprint(dealers_bp)
    app.register_blueprint(cars_bp)

    return app
