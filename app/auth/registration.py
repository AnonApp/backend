import bcrypt, uuid, secrets
import psycopg2
from twilio.rest import Client

class Registration():

    def __init__(self, email, phone_number, password):
        self.user_id = str(uuid.uuid4().hex)
        self.email = email
        self.phone_number = self.normalized_phone_number(phone_number)
        self.passhash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.user_key = str(secrets.token_hex(16))
    
    def do_registration(self):
        try:
            conn = psycopg2.connect(user = "postgres", host = "localhost", port = "5432", database = "anonimus")
            cursor = conn.cursor()
            register_query = """
                insert into users (user_id, phone_number, email, passhash, user_key) 
                values ('{}', '{}', '{}', '{}', '{}')
            """.format(self.user_id, self.phone_number, self.email, (self.passhash).decode('utf-8'), self.user_key)
            cursor.execute(register_query)
            conn.commit()
            self.send_otp_verification()
            return None
        except Exception as err:
            print("Error while creating PostgreSQL table: ", str(err))
            return str(err)
    
    def send_otp_verification(self):
        try:
            account_id = "AC9c7d3165a03e51dd55bb0f34cc77aaae"
            auth_token = "6b78e382cd366d14ada5908243c21f00"
            client = Client(account_id, auth_token)
            verification = client.verify.services("VA932bcc04550a6b6ae1aa243a38a93c4b").verifications.create(to=self.phone_number, channel='sms')
            return None
        except Exception as err:
            print("Error sending otp code: ", str(err))
            return 
    
    def normalized_phone_number(self, phone_number):
        if phone_number[0:2] == "08":
            return "+628"+phone_number[2:]
        