from hashlib import scrypt
from sql_alchemy import database
from sqlalchemy.sql.expression import func


class UserModel (database.Model):
    __tablename__ = 'users'
    id = database.Column(database.Integer, primary_key = True)
    name = database.Column(database.String(250))
    phone = database.Column(database.String(50))
    path = database.Column(database.String(250))
    email = database.Column(database.String(50))
    password = database.Column(database.String(250))

    def __init__(self, id, email, password, name, path, phone):
        self.id = id
        self.email = email
        self.password = password
        self.name = name
        self.path = path
        self.phone = phone



    def json(self):
        return {
            'id' : self.id,
            'name': self.name,
            'email' : self.email,
            'phone': self.phone,
            'path': self.path,
        }

    @classmethod  
    def find_user_by_id(cls, id): 
        user = cls.query.filter_by(id = id).first()
        if user:
            return user
        return None

    @classmethod  
    def find_user_by_email(cls, email): 
        user = cls.query.filter_by(email = email).first()
        if user:
            return user
        return None

    def save_user(self): 
        database.session.add(self)
        database.session.commit()

    def update_user(self, id, email, password, name, path, phone): 
        self.id = id
        self.email = email
        self.password = password
        self.name = name
        self.path = path
        self.phone = phone

    def delete_user(self): 
        database.session.delete(self)
        database.session.commit()
        
    @classmethod
    def find_last_user(cls):
        # id = database.engine.execute("select nextval('id') as new_id").fetchone() - postgres
        id = database.session.query(func.max(cls.id)).one()[0]

        if id:
            return id + 1
        return 1