from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # 👈 Agregado

db = SQLAlchemy()
migrate = Migrate()  # 👈 Agregado

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    migrate.init_app(app, db)  # 👈 Agregado

    from .routes import bp
    app.register_blueprint(bp)

    return app
