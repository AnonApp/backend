import os
import bcrypt
import psycopg2
import secrets

class Login():

    def __init__(self, phone_number='', password=''):
        self.phone_number = self.normalized_phone_number(phone_number)
        self.password = password
        self.db_conn = psycopg2.connect(os.environ['DATABASE_URL'])
        self.db_cursor = self.db_conn.cursor()

    def do_login(self):
        try:
            get_passhash_query = """SELECT passhash FROM users where phone_number='{}' """.format(self.phone_number)
            self.db_cursor.execute(get_passhash_query)
            passhash = self.db_cursor.fetchone()[0]
            if bcrypt.checkpw((self.password).encode('utf-8'), (passhash).encode('utf-8')):
                user_key = str(secrets.token_hex(16))
                update_user_key_query = "UPDATE users SET user_key=%s, updated_at=Now() WHERE phone_number=%s;"
                self.db_cursor.execute(update_user_key_query, (user_key, self.phone_number))
                self.db_conn.commit()
                return False, user_key
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