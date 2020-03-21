import json
from flask import request, Response
from app.auth import auth_bp

@auth_bp.route("/api/register", methods=["POST"])
def RegistrationController():
    req = request.get_json()
    res = {
        "success": True,
        "message": "We receive the input",
        "email": req['email'],
        "phone_number": req['phone_number']
    }
    return Response(json.dumps(res, sort_keys=False), mimetype='application/json')
    


