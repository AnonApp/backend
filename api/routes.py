from flask import Blueprint, request

api_routes = Blueprint('api', __name__)

#PING ROUTE
@api_routes.route("/api/ping", methods=['GET'])
def PingController():
    res = {
        "response": "PONG!"
    }
    return res
