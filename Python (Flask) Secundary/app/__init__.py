import os
from flask import Flask
from flask_cors import CORS
from .config import Config
from .extensions import db, migrate
from .errors import errors_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    origins = app.config.get("CORS_ORIGINS") or True
    CORS(app, resources={r"/*": {"origins": origins}}, supports_credentials=True)

    from .modules.brands.routes import bp as brands_bp
    from .modules.models.routes import bp as models_bp
    from .modules.cars.routes    import bp as cars_bp

    app.register_blueprint(errors_bp)
    app.register_blueprint(brands_bp, url_prefix="/brands")
    app.register_blueprint(models_bp, url_prefix="/models")
    app.register_blueprint(cars_bp,   url_prefix="/cars")
    return app
