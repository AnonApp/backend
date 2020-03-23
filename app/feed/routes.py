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
            "success": False,
            "message": "user is not logged in.",
            "redirect_to": "APP_URL_FOR_LOGIN"
        }
        if Login().verify_login(req['user_key']) is False:
            return Response(json.dumps(res, sort_keys=False), mimetype='application/json')
        
        res["success"]= True,
        res["message"]= "Here is the feed:",
        res["redirect_to"]= "",
        res["feed"] = Feed().get_feed()
        return Response(json.dumps(res, sort_keys=False), mimetype='application/json')

        
            