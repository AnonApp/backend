import bcrypt
import psycopg2

class Login():

    def __init__(self, phone_number, password):
        self.phone_number = self.normalized_phone_number(phone_number)
        self.password = password

    def do_login(self):
        try:
            conn = psycopg2.connect(user = "postgres", host = "localhost", port = "5432", database = "anonimus")
            cursor = conn.cursor()
            get_passhash_query = """SELECT passhash FROM users where phone_number='{}' """.format(self.phone_number)
            cursor.execute(get_passhash_query)
            passhash = cursor.fetchone()[0]
            if bcrypt.checkpw((self.password).encode('utf-8'), (passhash).encode('utf-8')):
                get_user_key_query = """SELECT user_key FROM users where phone_number='{}' """.format(self.phone_number)
                cursor.execute(get_user_key_query)
                return False, cursor.fetchone()[0]
        except Exception as err:
            print("Error while fetching PostgreSQL table: ", str(err))
            return True, str(err)

    def normalized_phone_number(self, phone_number):
        if phone_number[0:2] == "08":
            return "+628"+phone_number[2:]