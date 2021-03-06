import os
import psycopg2
from twilio.rest import Client

class OTP():

    def __init__(self, phone_number):
        self.phone_number = self.normalized_phone_number(phone_number)
        self.account_id = "AC9c7d3165a03e51dd55bb0f34cc77aaae"
        self.auth_token = "5d2ab36375d66f1e575d186ca1d3c5f8" #this has been rotated
        self.service_code = "VAe7ca0f26de0745424a9ca6dcf42b8fa9" #rotate this again
        self.client = Client(self.account_id, self.auth_token)

    def do_create_new_service(self):
        service = self.client.verify.services.create(friendly_name='Anonimus', code_length=4)
        self.service_code = service.sid

    def do_send_code(self):
        try:
            verification = self.client.verify.services(self.service_code).verifications.create(to=self.phone_number, channel='sms')
            return None
        except Exception as err:
            print("Error sending otp code: ", str(err))
            return str(err)
    
    def do_verify(self, otp_code):
        try:
            verification_check = self.client.verify.services(self.service_code).verification_checks.create(to=self.phone_number, code=otp_code)
            if verification_check.valid:
                conn = psycopg2.connect(os.environ['DATABASE_URL'])
                cursor = conn.cursor()
                verified_query = """UPDATE users SET is_verified=true, updated_at=Now() WHERE phone_number='{}';""".format(self.phone_number)
                cursor.execute(verified_query)
                conn.commit()
        except Exception as err:
            print("Error when verifying otp code: ", str(err))
            return str(err)
    
    def normalized_phone_number(self, phone_number):
        if phone_number[0:2] == "08":
            return "+628"+phone_number[2:]
        return phone_number
