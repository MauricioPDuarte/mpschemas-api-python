from models.brand import BrandModel
from models.model import ModelModel
from models.type_device import TypeDeviceModel
from models.user import UserModel
from sql_alchemy import database

class SchemaModel(database.Model):
    __tablename__ = 'schema'
    id = database.Column(database.Integer, primary_key = True)
    model_id = database.Column(database.Integer, database.ForeignKey('model.id'))
    type_device_id = database.Column(database.Integer, database.ForeignKey('type_device.id'))
    brand_id = database.Column(database.Integer, database.ForeignKey('brand.id'))
    user_id = database.Column(database.Integer, database.ForeignKey('users.id'))
    path = database.Column(database.String(250))
    model = database.relationship(ModelModel, backref=('model'))
    type_device = database.relationship(TypeDeviceModel, backref=('type_device'))
    user = database.relationship(UserModel, backref=('user'))
    brand = database.relationship(BrandModel, backref=('brand1'))

    def __init__(self, type_device_id, user_id, model_id, brand_id, path):
        self.model_id = model_id
        self.type_device_id = type_device_id
        self.user_id = user_id
        self.brand_id = brand_id
        self.path = path

    def json(self): 
        return {
            'id': self.id,
            'type_device_id': self.type_device_id,
            'user_id': self.user_id,
            'model_id': self.model_id,
            'brand_id': self.brand_id,
            'user': {
                'id': self.user.id,
                'name': self.user.name,
                'email': self.user.email,
            },
            'type_device': {
                'id': self.type_device.id,
                'name': self.type_device.name,
            },
            'model': {
                'id': self.model.id,
                'name': self.model.name,
            },
            'brand': {
                'id': self.brand.id,
                'name': self.brand.name,
            },
            'path': self.path
        }

    @classmethod  
    def find_by_id(cls, id):
        schema = cls.query.filter_by(id = id).first() 
        if schema:
            return schema
        return None

    def save(self): 
        database.session.add(self)
        database.session.commit()

    def update(self, type_device_id, brand_id, model_id, user_id, path): 
        self.type_device_id = type_device_id
        self.brand_id = brand_id
        self.model_id = model_id
        self.user_id = user_id
        self.path = path

    def delete(self): 
        database.session.delete(self)
        database.session.commit()
