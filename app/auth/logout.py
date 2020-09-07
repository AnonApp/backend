import os
import psycopg2

class Logout():

    def __init__(self, phone_number):
        self.phone_number = self.normalized_phone_number(phone_number)
    
    def do_logout(self):
        try:
            conn = psycopg2.connect(os.environ['DATABASE_URL'])
            cursor = conn.cursor()
            update_user_key_query = """UPDATE users SET user_key='', updated_at=Now() WHERE phone_number='{}';""".format(self.phone_number)
            cursor.execute(update_user_key_query)
            conn.commit()
            return False, None
        except Exception as err:
            print("Error when logging out: ", str(err))
            return True, str(err)
    
    def normalized_phone_number(self, phone_number):
        if phone_number[0:2] == "08":
            return "+628"+phone_number[2:]
        return phone_number