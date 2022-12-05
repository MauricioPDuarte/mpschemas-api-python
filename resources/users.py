import os
import uuid
from flask_restful import Resource, reqparse
from models.user import UserModel
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.datastructures import FileStorage
from utils import allowed_file
from flask import current_app

minha_requisicao = reqparse.RequestParser()
minha_requisicao.add_argument('email', location='form', type=str, required=True, help="email is required")
minha_requisicao.add_argument('name', location='form', type=str, required=True, help="name is required")
minha_requisicao.add_argument('phone', location='form', type=str, required=True, help="phone is required")
minha_requisicao.add_argument('password', location='form', type=str, required=True, help="password is required")
minha_requisicao.add_argument('file', type=FileStorage, location='files',  required=False)


class Users(Resource):
     def get(self):
        return {'data': [device.json() for device in UserModel.query.all()], 'code': 200}

class User(Resource):
    def put(self, id):
        dados = minha_requisicao.parse_args()
        user = UserModel.find_user_by_id(id)
        if user:
            if dados.password:
                passwordHashad = generate_password_hash(dados.password)
                dados["password"] = passwordHashad
            else:
                dados["password"] = user.password

            filename = user.path
            if dados.file and allowed_file(dados.file.filename):
                filename = str(uuid.uuid4()) + '-' + dados.file.filename
                path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                dados.file.save(path)

                if user.path:
                    oldpath = os.path.join(current_app.config['UPLOAD_FOLDER'], user.path)
                    os.remove(oldpath)

            user.update_user(id, dados.email, dados.password, dados.name, filename, dados.phone)
            user.save_user()
            return {'data': 'success', 'code': 200}, 200
        return {'data': 'user not found', 'code': 404}, 404



    def get(self, id):
        user = UserModel.find_user_by_id(id)
        if user: 
            return {'data': user.json(), 'code': 200}, 200
        return {'data':'user not found', 'code': 404}, 404 # or 204

    def delete(self, id):
        user = UserModel.find_user_by_id(id)
        if user:
            user.delete_user()
            return {'data' : 'user deleted', 'code': 200}, 200
        return {'data' : 'user not founded', 'code': 404}, 404

    def post(self, id):
        dados = minha_requisicao.parse_args()

        if UserModel.find_user_by_email(dados['email']):
            return {'data':'EMAIL_EXISTS'.format(dados['email']), 'code': 400}, 400

        id = UserModel.find_last_user()

        passwordHashad = generate_password_hash(dados.password)

        file = dados.file
        filename = None
        if file and allowed_file(file.filename):
            filename = str(uuid.uuid4()) + '-' + dados.file.filename
            path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(path)


        new_user = UserModel(id, dados.email, passwordHashad, dados.name, filename, dados.phone)
        
        try:
            print(new_user.json())
            new_user.save_user()
        except:
            return {'data':'An internal error ocurred.', 'code': 500}, 500

        return {'data': new_user.json(), 'code': 201}, 201