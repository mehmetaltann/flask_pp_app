from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

login_manager = LoginManager()
db = SQLAlchemy(session_options={"autoflush": False})
bootstrap = Bootstrap()

