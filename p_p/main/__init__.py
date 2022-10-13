from flask import Blueprint

main = Blueprint("main", __name__)

from p_p.main import routes