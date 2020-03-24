import bcrypt
import psycopg2
import secrets
import datetime
from app.models import db, Users

class Login():

    def __init__(self, phone_number='', password=''):
        self.phone_number = self.normalized_phone_number(phone_number)
        self.password = password

    def do_login(self):
        try:
            user = db.session.query(Users).filter_by(phone_number=self.phone_number).first()
            if bcrypt.checkpw((self.password).encode('utf-8'), (user.passhash).encode('utf-8')):
                token = str(secrets.token_hex(16))
                db.session.query(Users).filter_by(phone_number=self.phone_number).update({"token": token,  "updated_at": datetime.datetime.utcnow()})
                db.session.commit()
                return False, token
        except Exception as err:
            print("Error while logging in: ", str(err))
            return True, str(err)
    
    def verify_login(self, token):
        try:
            count = db.session.query(Users).filter_by(token=token).count()
            if count < 1:
                return False
            return True
        except Exception as err:
            print("Error when verifying login: ", str(err))
            return False

    def normalized_phone_number(self, phone_number):
        if phone_number[0:2] == "08":
            return "+628"+phone_number[2:]
        return phone_number