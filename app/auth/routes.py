import json
import psycopg2
from flask import request, Response
from app.auth import auth_bp
from app.auth.registration import Registration

@auth_bp.route("/api/register", methods=["POST"])
def RegistrationController():
    req = request.get_json()
    res = {
        "success": True,
        "message": "Success! Welcome to the family!",
        "email": req['email'],
        "phone_number": req['phone_number']
    }

    err = Registration(req['email'], req['phone_number'], req['password']).do_registration()
    if err is not None:
        res["success"] = False
        res["message"] = err

    return Response(json.dumps(res, sort_keys=False), mimetype='application/json')
    


