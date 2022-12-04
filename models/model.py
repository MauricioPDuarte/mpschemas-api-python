from xmlrpc.client import DateTime
from models.brand import BrandModel
from sql_alchemy import database
from sqlalchemy.sql import func

class ModelModel(database.Model): 
    __tablename__ = 'model'
    id = database.Column(database.Integer, primary_key = True)
    name = database.Column(database.String(250))
    brand_id = database.Column(database.Integer, database.ForeignKey('brand.id'))
    brand = database.relationship(BrandModel, backref=('brand'))
    created_on = database.Column(database.DateTime, server_default=database.func.now())
    updated_on = database.Column(database.DateTime, server_default=database.func.now(), server_onupdate=database.func.now())


    def __init__(self, name, brand_id):
        self.name = name
        self.brand_id = brand_id

    def json(self): 
        return {'id': self.id, 'name': self.name, 'brand_id': self.brand_id, 'brand': { 'id': self.brand.id, 'name': self.brand.name}, 'created_on': self.created_on.strftime("%d-%m-%Y %H:%M:%S"), 'updated_on': self.updated_on.strftime("%d-%m-%Y %H:%M:%S"),}

    @classmethod  
    def find_by_id(cls, id):
        schema = cls.query.filter_by(id = id).first() 
        if schema:
            return schema
        return None

    def save(self): 
        database.session.add(self)
        database.session.commit()

    def update(self, name, brand_id): 
        self.name = name
        self.brand_id = brand_id

    def delete(self): 
        database.session.delete(self)
        database.session.commit()

