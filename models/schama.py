from sql_alchemy import database

class SchemaModel(database.Model):
    __tablename__ = 'schema'
    id = database.Column(database.Integer, primary_key = True)
    name = database.Column(database.String(250))

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def json(self): 
        return {'id': self.id, 'name': self.name}

    @classmethod  
    def find_schema_by_id(cls, id):
        schema = cls.query.filter_by(id = id).first() 
        if schema:
            return schema
        return None

    def save_schema(self): 
        database.session.add(self)
        database.session.commit()

    def update_schema(self, name, rating, duration): 
        self.name = name
        self.rating = rating
        self.duration = duration

    def delete_schema(self): 
        database.session.delete(self)
        database.session.commit()

    @classmethod
    def find_last_movie(cls):
        schema_id = database.engine.execute("select max('id') as new_id from schema").fetchone() 
        if schema_id:
            return schema_id['new_id'] + 1
        return 1