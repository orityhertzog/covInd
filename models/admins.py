from common.database import Database
from common.utils import Utils


class Admin:
    def __init__(self, email, password):
        self.email = email
        self.password = Utils.encrypt_pass(password)

    @staticmethod
    def login_valid(email, password):
        user = Database.find_one_by('admins', {"email": email})
        if not Utils.unencrypt_pass(password=password, encrypt_password=user['password']):
            return False
        return True

    @staticmethod
    def register(email, items):
        user = Database.find_one_by('admins', {"email": email})
        if user is not None:
            return False
        else:
            Database.insert('admins', items)
            return True

    @staticmethod
    def toJson(full_name, email, password):
        return {
            "full_name": full_name,
            "email": email,
            "password": password
        }

    @staticmethod
    def sum_tickets_amount(collection):
        pipeline = [{'$group': {'_id': None, 'amount': {'$sum': '$tickets_amount'}}}]
        sum_tickets_amount = list(Database.DATABASE[collection].aggregate(pipeline=pipeline))
        if len(sum_tickets_amount) > 0:
            return sum_tickets_amount[0]['amount']
        else:
            return 0

    @staticmethod
    def tickets_by_name(collection):
        pipeline = [{'$group': {'_id': '$full_name', 'amount': {'$first': "$tickets_amount"}}}]
        tickets_by_name = list(Database.DATABASE[collection].aggregate(pipeline=pipeline))
        return tickets_by_name

    @staticmethod
    def equipment_amount(collection):
        mat_pipeline = [{'$group': {'_id': None, 'amount': {'$sum': '$mat'}}}]
        food_pipeline = [{'$group': {'_id': None, 'amount': {'$sum': '$food'}}}]
        instrument_pipeline = [{'$group': {'_id': None, 'amount': {'$sum': '$instrument'}}}]
        camp_pipeline = [{'$group': {'_id': None, 'amount': {'$sum': '$camp'}}}]
        mat_amount = list(Database.DATABASE[collection].aggregate(mat_pipeline))
        food_amount = list(Database.DATABASE[collection].aggregate(food_pipeline))
        instrument_amount = list(Database.DATABASE[collection].aggregate(instrument_pipeline))
        camp_amount = list(Database.DATABASE[collection].aggregate(camp_pipeline))
        equipments = [mat_amount[0]['amount'] if len(mat_amount) > 0 else 0,
                      food_amount[0]['amount'] if len(mat_amount) > 0 else 0,
                      instrument_amount[0]['amount'] if len(mat_amount) > 0 else 0,
                      camp_amount[0]['amount'] if len(mat_amount) > 0 else 0]
        return equipments
