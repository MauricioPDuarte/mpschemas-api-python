from xmlrpc.client import DateTime
from sql_alchemy import database
from sqlalchemy.sql import func


class ForgotPasswordModel(database.Model): 
    __tablename__ = 'forgot_password'
    id = database.Column(database.Integer, primary_key = True)
    code = database.Column(database.String(250))
    user_id = database.Column(database.Integer)
    created_on = database.Column(database.DateTime, server_default=database.func.now())
    updated_on = database.Column(database.DateTime, server_default=database.func.now(), server_onupdate=database.func.now())

    def __init__(self, code, user_id):
        self.code = code
        self.user_id = user_id

    @classmethod  
    def find_by_code(cls, code):
        res = cls.query.filter_by(code = code).first() 
        if res:
            return res
        return None

    def save(self): 
        database.session.add(self)
        database.session.commit()

