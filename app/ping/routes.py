from app.ping import ping_bp

@ping_bp.route("/api/ping", methods=['GET'])
def PingController():
    res = {
        "response": "PONG!"
    }
    return res
