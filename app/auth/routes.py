from flask import request
from app.auth import auth_bp

@auth_bp.route("/api/register", methods=["POST"])
def RegistrationController():
    body = request.get_json()
    res = {
        "response": "Success!",
        "message": body
    }
    return res
