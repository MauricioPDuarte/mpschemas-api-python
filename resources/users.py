from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_jwt_extended import create_access_token

minha_requisicao = reqparse.RequestParser()
minha_requisicao.add_argument('email', type=str, required=True, help="email is required")
minha_requisicao.add_argument('name', type=str, required=True, help="name is required")
minha_requisicao.add_argument('password', type=str, required=True, help="password is required")


class Users(Resource):
     def get(self):
        return {'data': [device.json() for device in UserModel.query.all()], 'code': 200}

class User(Resource):
    def put(self, id):
        dados = minha_requisicao.parse_args()
        user = UserModel.find_user_by_id(id)
        if user:
            user.update_user(id, **dados)
            user.save_user()
            return user.json(), 200

        id = UserModel.find_last_user()
        new_user = UserModel(id, **dados)
        new_user.save_user()
        return new_user.json(), 201

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
            return {'data':'email {} already exists'.format(dados['email']), 'code': 200}, 200

        id = UserModel.find_last_user()

        new_user = UserModel(id, **dados)
        
        try:
            print(new_user.json())
            new_user.save_user()
        except:
            return {'data':'An internal error ocurred.', 'code': 500}, 500

        return {'data': new_user.json(), 'code': 201}, 201