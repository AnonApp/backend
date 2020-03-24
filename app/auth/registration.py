import bcrypt, uuid, secrets
import psycopg2
from twilio.rest import Client
from app.auth.otp import OTP
from app.models import db, Users

class Registration():

    def __init__(self, email, phone_number, password):
        self.user_id = str(uuid.uuid4().hex)
        self.email = email
        self.phone_number = self.normalized_phone_number(phone_number)
        self.passhash = (bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())).decode('utf-8')
        self.token = str(secrets.token_hex(16))
    
    def do_registration(self):
        print((self.passhash).encode('utf-8'))
        try:
            user = Users(id=self.user_id, phone_number=self.phone_number, email=self.email, passhash=(self.passhash), token=self.token)
            db.session.add(user)
            db.session.commit()
            # OTP(self.phone_number).do_send_code()
            return None
        except Exception as err:
            return str(err)
    
    def normalized_phone_number(self, phone_number):
        if phone_number[0:2] == "08":
            return "+628"+phone_number[2:]
        return phone_number
        