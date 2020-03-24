import json
import psycopg2
from flask import request, Response
from app.feed import feed_bp
from app.auth.login import Login
from app.feed.feed import Feed

@feed_bp.route("/api/feed", methods=["POST"])
def FeedController():
    req = request.get_json()
    res = {
        "success": True,
    }
    if Login().verify_login(req['user_key']) is False:
        res["message"] = "User is not logged in",
        res["redirect_to"]= "APP_URL",
        return Response(json.dumps(res, sort_keys=False), mimetype='application/json')
    
    res["feed"] = Feed(req['user_key']).get_feed()
    return Response(json.dumps(res, sort_keys=False), mimetype='application/json')

@feed_bp.route("/api/feed/post", methods=["POST"])
def PostController():
    req = request.get_json()
    res = {
        "succces": True
    }
    if Login().verify_login(req['user_key']) is False:
        res["message"] = "User is not logged in",
        res["redirect_to"]= "APP_URL",
        return Response(json.dumps(res, sort_keys=False), mimetype='application/json')
    
    err, err_message = Feed(req['user_key']).submit_post(req['post_content'])
    if err:
        res['success'] = False
        res['message'] = err_message
        return Response(json.dumps(res, sort_keys=False), mimetype='application/json')
    res['message'] = err_message
    return Response(json.dumps(res, sort_keys=False), mimetype='application/json')

    
        
            