import json
import psycopg2
from flask import request, Response
from app.auth import auth_bp
from app.auth.registration import Registration
from app.auth.otp import OTP

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

@auth_bp.route("/api/otp", methods=["POST"])
def OTPController():
    req = request.get_json()
    res = {
        "success": True,
        "message": "The number is succesfully verified!",
        "phone_number": req['phone_number'],
        "otp_code": req['otp_code']
    }

    err = OTP(req['phone_number']).do_verify(req['otp_code'])
    if err is not None:
        res["success"] = False
        res["message"] = err

    return Response(json.dumps(res, sort_keys=False), mimetype='application/json')


    


