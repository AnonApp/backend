from flask import Blueprint, request

ping_routes = Blueprint('api', __name__)

#PING ROUTE
@ping_routes.route("/api/ping", methods=['GET'])
def PingController():
    res = {
        "response": "PONG!"
    }
    return res
