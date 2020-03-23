import json
import psycopg2
from flask import request, Response
from app.feed import feed_bp
from app.auth.login import Login
from app.feed.feed import Feed

@feed_bp.route("/api/feed", methods=["GET", "POST"])
def FeedController():
    if request.method == "POST":
        req = request.get_json()
        res = {
            "success": True,
        }
        if Login().verify_login(req['user_key']) is False:
            res["message"] = "User is not logged in",
            res["redirect_to"]= "APP_URL",
            return Response(json.dumps(res, sort_keys=False), mimetype='application/json')
        
        res["feed"] = Feed().get_feed()
        return Response(json.dumps(res, sort_keys=False), mimetype='application/json')

        
            