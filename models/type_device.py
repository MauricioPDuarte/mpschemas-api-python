from xmlrpc.client import DateTime
from sql_alchemy import database
from sqlalchemy.sql import func

class TypeDeviceModel(database.Model): 
    __tablename__ = 'type_device'
    id = database.Column(database.Integer, primary_key = True)
    name = database.Column(database.String(250))
    created_on = database.Column(database.DateTime, server_default=database.func.now())
    updated_on = database.Column(database.DateTime, server_default=database.func.now(), server_onupdate=database.func.now())

    def __init__(self, name):
        self.name = name

    def json(self): 
        return {'id': self.id, 'name': self.name, 'created_on': self.created_on.strftime("%d-%m-%Y %H:%M:%S"), 'updated_on': self.updated_on.strftime("%d-%m-%Y %H:%M:%S"),}

    @classmethod  
    def find_type_device_by_id(cls, id):
        schema = cls.query.filter_by(id = id).first() 
        if schema:
            return schema
        return None

    def save_type_device(self): 
        database.session.add(self)
        database.session.commit()

    def update_type_device(self, name, rating, duration): 
        self.name = name
        self.rating = rating
        self.duration = duration

    def delete_type_device(self): 
        database.session.delete(self)
        database.session.commit()

