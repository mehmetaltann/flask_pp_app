from flask import Flask
from .extensions import db, login_manager, bootstrap
from .commands import create_tables
from .main import main
from .login import giris

def create_app(config_file='settings.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    db.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    app.register_blueprint(main)
    app.register_blueprint(giris)
    app.jinja_env.cache = {}
    app.cli.add_command(create_tables)
    
    # Tablolarda ki TL değerler için
    @app.template_filter()
    def currencyFormat(value):
        value = float(value)
        return f"{value} TL"
    
    return app

