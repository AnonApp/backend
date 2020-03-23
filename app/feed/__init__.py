from flask import Blueprint

feed_bp = Blueprint('feed', __name__)

from app.feed import routes