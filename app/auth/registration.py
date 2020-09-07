import bcrypt, uuid, secrets
import psycopg2
import os
# from twilio.rest import Client
# from app.auth.otp import OTP

class Registration():

    def __init__(self, email, phone_number, password):
        self.user_id = str(uuid.uuid4().hex)
        self.email = email
        self.phone_number = self.normalized_phone_number(phone_number)
        self.passhash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.user_key = str(secrets.token_hex(16))
    
    def do_registration(self):
        try:
            conn = psycopg2.connect(os.environ['DATABASE_URL'])
            cursor = conn.cursor()
            register_query = """
                INSERT INTO users (user_id, phone_number, email, passhash, user_key) 
                VALUES ('{}', '{}', '{}', '{}', '{}')
            """.format(self.user_id, self.phone_number, self.email, (self.passhash).decode('utf-8'), self.user_key)
            cursor.execute(register_query)
            conn.commit()
            # OTP(self.phone_number).do_send_code() #raise exception
            return None
        except Exception as err:
            print("Error while creating PostgreSQL table: ", str(err))
            return str(err)
    
    def normalized_phone_number(self, phone_number):
        if phone_number[0:2] == "08":
            return "+628"+phone_number[2:]
        return phone_number
        