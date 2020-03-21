from flask import Blueprint

ping_bp = Blueprint('ping', __name__)

from app.ping import routes