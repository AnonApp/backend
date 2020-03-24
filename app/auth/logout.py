import datetime
from app.models import db, Users

class Logout():

    def __init__(self, phone_number):
        self.phone_number = self.normalized_phone_number(phone_number)
    
    def do_logout(self):
        try:
            db.session.query(Users).filter_by(phone_number=self.phone_number).update({"token": '', "updated_at": datetime.datetime.utcnow()})
            db.session.commit()
            return False, None
        except Exception as err:
            print("Error when logging out: ", str(err))
            return True, str(err)
    
    def normalized_phone_number(self, phone_number):
        if phone_number[0:2] == "08":
            return "+628"+phone_number[2:]
        return phone_number