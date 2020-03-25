import json
import psycopg2
from flask import request, Response
from app.feed import feed_bp
from app.auth.login import Login
from app.feed.feed import Feed

@feed_bp.route("/api/feed/getposts", methods=["POST"])
def GetPostController():
    req = request.get_json()
    res = {
        "success": True,
    }
    if Login().verify_login(req['token']) is False:
        res["message"] = "User is not logged in",
        res["redirect_to"]= "APP_URL",
        return Response(json.dumps(res, sort_keys=False), mimetype='application/json')
    
    res["feed"] = Feed(req['token']).get_posts()
    return Response(json.dumps(res, sort_keys=False), mimetype='application/json')

@feed_bp.route("/api/feed/submitpost", methods=["POST"])
def SubmitPostController():
    req = request.get_json()
    res = {
        "succces": True
    }
    if Login().verify_login(req['token']) is False:
        res["message"] = "User is not logged in",
        res["redirect_to"]= "APP_URL",
        return Response(json.dumps(res, sort_keys=False), mimetype='application/json')
    
    err, err_message = Feed(req['token']).submit_post(req['post_content'])
    if err:
        res['success'] = False
        res['message'] = err_message
        return Response(json.dumps(res, sort_keys=False), mimetype='application/json')
    res['message'] = err_message
    return Response(json.dumps(res, sort_keys=False), mimetype='application/json')

@feed_bp.route("/api/feed/getcomments", methods=["POST"])
def GetCommentController():
    req = request.get_json()
    res = {
        "success": True,
    }
    if Login().verify_login(req['token']) is False:
        res["message"] = "User is not logged in",
        res["redirect_to"]= "APP_URL",
        return Response(json.dumps(res, sort_keys=False), mimetype='application/json')
    
    res["comments"] = Feed(req['token']).get_comments(req['post_id'])
    return Response(json.dumps(res, sort_keys=False), mimetype='application/json')

@feed_bp.route("/api/feed/submitcomment", methods=["POST"])
def SubmitCommentController():
    req = request.get_json()
    res = {
        "succces": True
    }
    if Login().verify_login(req['token']) is False:
        res["message"] = "User is not logged in",
        res["redirect_to"]= "APP_URL",
        return Response(json.dumps(res, sort_keys=False), mimetype='application/json')
    
    err, err_message = Feed(req['token']).submit_comment(req['post_id'], req['comment_content'])
    if err:
        res['success'] = False
        res['message'] = err_message
        return Response(json.dumps(res, sort_keys=False), mimetype='application/json')
    res['message'] = err_message
    return Response(json.dumps(res, sort_keys=False), mimetype='application/json')

@feed_bp.route("/api/feed/submitlike", methods=["POST"])
def SubmitLikeController():
    req = request.get_json()
    res = {
        "success": True
    }
    if Login().verify_login(req['token']) is False:
        res["message"] = "User is not logged in",
        res["redirect_to"]= "APP_URL",
        return Response(json.dumps(res, sort_keys=False), mimetype='application/json')
        
    err, err_message = Feed(req['token']).submit_like(req["post_id"], req["comment_id"])
    if err:
        res['success'] = False
        res['message'] = err_message
        return Response(json.dumps(res, sort_keys=False), mimetype='application/json')
    res['message'] = err_message
    return Response(json.dumps(res, sort_keys=False), mimetype='application/json')

@feed_bp.route("/api/feed/submitunlike", methods=["POST"])
def SubmitUnlikeController():
    req = request.get_json()
    res = {
        "success": True
    }
    if Login().verify_login(req['token']) is False:
        res["message"] = "User is not logged in",
        res["redirect_to"]= "APP_URL",
        return Response(json.dumps(res, sort_keys=False), mimetype='application/json')
        
    err, err_message = Feed(req['token']).submit_unlike(req["post_id"], req["comment_id"])
    if err:
        res['success'] = False
        res['message'] = err_message
        return Response(json.dumps(res, sort_keys=False), mimetype='application/json')
    res['message'] = err_message
    return Response(json.dumps(res, sort_keys=False), mimetype='application/json')