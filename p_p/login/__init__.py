from flask import Blueprint

giris = Blueprint("giris", __name__)

from p_p.login import routes