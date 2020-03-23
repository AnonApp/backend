import json
import psycopg2
from flask import request, Response
from app.auth import auth_bp
from app.auth.registration import Registration
from app.auth.otp import OTP
from app.auth.login import Login
from app.auth.logout import Logout

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

@auth_bp.route("/api/login", methods=["POST"])
def LoginController():
    req = request.get_json()
    res = {
        "success": True,
        "message": "Login succesfull",
        "user_key": "null"
    }

    err, message = Login(req['phone_number'], req['password']).do_login()
    if err:
        res["success"] = False
        res["message"] = message
    else:
        res['user_key'] = message

    return Response(json.dumps(res, sort_keys=False), mimetype='application/json')

@auth_bp.route("/api/login/verify", methods=["POST"])
def VerifyLoginController():
    req = request.get_json()
    res = {
        "success": True,
        "message": "You are logged in."
    }

    if Login().verify_login(req['user_key']) is False:
        res['message'] = "I'm sorry, who are you?"

    return Response(json.dumps(res, sort_keys=False), mimetype='application/json')

@auth_bp.route("/api/logout", methods=["POST"])
def LogoutController():
    req = request.get_json()
    res = {
        "success": True,
        "message": "Logout succesfull, see you later!"
    }

    err, err_message = Logout(req['phone_number']).do_logout()
    if err:
        res["success"] = False
        res["message"] = err_message
    
    return Response(json.dumps(res, sort_keys=False), mimetype='application/json')
