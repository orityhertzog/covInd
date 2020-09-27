from common.database import Database
from common.utils import Utils


class Users:

    @staticmethod
    def register(email, items):
        user = Database.find_one_by('participants', {"email": email})
        if user is not None:
            return False
        else:
            Database.insert('participants', items)
            return True

    @staticmethod
    def login_valid(email, password):
        user = Database.find_one_by('participants', {'email': email})
        if not Utils.unencrypt_pass(password=password, encrypt_password=user['password']):
            return False
        return True

    @staticmethod
    def toJson(full_name, email, password, tickets_amount, mat, instrument, food, camp):
        return {
            'full_name': full_name,
            'email': email,
            'password': password,
            'tickets_amount': int(tickets_amount),
            'mat': mat,
            'instrument': instrument,
            'food': food,
            'camp': camp
        }
