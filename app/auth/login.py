import bcrypt
import psycopg2
import secrets
from app.models import db, Users

class Login():

    def __init__(self, phone_number='', password=''):
        self.phone_number = self.normalized_phone_number(phone_number)
        self.password = password
        self.db_conn = psycopg2.connect(user = "postgres", host = "localhost", port = "5432", database = "anonimus")
        self.db_cursor = self.db_conn.cursor()

    def do_login(self):
        try:
            user = db.session.query(Users).filter_by(phone_number=self.phone_number).first()
            if bcrypt.checkpw((self.password).encode('utf-8'), (user.passhash).encode('utf-8')):
                token = str(secrets.token_hex(16))
                db.session.query(Users).filter_by(phone_number=self.phone_number).update({"token": token})
                db.session.commit()
                return False, token
        except Exception as err:
            print("Error while logging in: ", str(err))
            return True, str(err)
    
    def verify_login(self, user_key):
        try:
            count_key_query = "select count(*) from users where user_key='{}';".format(user_key)
            self.db_cursor.execute(count_key_query)
            if int(self.db_cursor.fetchone()[0]) is 0:
                return False
            return True
        except Exception as err:
            print("Error when verifying login: ", str(err))
            return False

    def get_user(self, user_key):
        try:
            count_key_query = "select user_id, phone_number, email from users where user_key='{}';".format(user_key)
            self.db_cursor.execute(count_key_query)
            query_result = self.db_cursor.fetchone()
            return True, query_result
        except Exception as err:
            print("Error when verifying login: ", str(err))
            return False, str(err)

    def normalized_phone_number(self, phone_number):
        if phone_number[0:2] == "08":
            return "+628"+phone_number[2:]
        return phone_number