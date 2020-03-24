import bcrypt, uuid, secrets
import psycopg2
from twilio.rest import Client
from app.auth.otp import OTP
# from app import db
# from app.models import Users

class Registration():

    def __init__(self, email, phone_number, password):
        self.user_id = str(uuid.uuid4().hex)
        self.email = email
        self.phone_number = self.normalized_phone_number(phone_number)
        self.passhash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.user_key = str(secrets.token_hex(16))
    
    # def do_registration(self):
        # user = Users()
    
    def normalized_phone_number(self, phone_number):
        if phone_number[0:2] == "08":
            return "+628"+phone_number[2:]
        return phone_number
        