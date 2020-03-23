import json
import psycopg2
from flask import request, Response
from app.feed import feed_bp

# @feed_bp.route("/api/feed", methods=["GET", "POST"])
# def FeedController():
#     if request.method == "POST":
#         req = request.get_json()
        