from datetime import datetime, timedelta
import random
import uuid
from flask import Flask, make_response, jsonify, request, send_from_directory
from flask_restful import Api
from werkzeug.security import generate_password_hash, check_password_hash


from flask_jwt_extended import JWTManager
from models.forgot_password import ForgotPasswordModel
from models.user import UserModel
from resources.brand import Brand, Brands
from resources.model import Model, Models
from resources.schema import Schema, Schemas
from resources.type_device import TypeDevice, TypesDevice
from flask_cors import CORS, cross_origin
from flask_mail import Mail, Message

from resources.users import User, Users
from resources.users_session import UserSession

UPLOAD_FOLDER = 'assets/uploads'



app = Flask(__name__)
api = Api(app)
cors = CORS(app)
jwt = JWTManager(app)


# Configs
app.config['JSON_SORT_KEYS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/mpschemas?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'mpschemas2022trabalhoaulafacul'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'mpschemas@gmail.com'
app.config['MAIL_PASSWORD'] = 'wztfceqkmuchcwcm'

mail = Mail(app)




@app.route("/files/<path:path>")
def get_file(path):
    """Download a file."""
    return send_from_directory(UPLOAD_FOLDER, path, as_attachment=True)


@app.route("/forgot_password", methods=['POST'])
def post():
    content = request.json
    userEmail = content["email"]
    user = UserModel.find_user_by_email(userEmail)
    if user:
        code = ""
        for i in range(5):
            temp = str(random.randint(0, 9))
            code += temp

        forgotPassword = ForgotPasswordModel(code, user.id)
        forgotPassword.save()

        # passwordHashad = generate_password_hash(senha)
        # user.update_user(user.id, user.email, passwordHashad, user.name)
        # user.save_user()

        msg = Message('Recuperação de senha', sender =   'mpschemas@gmail.com', recipients = [user.email])
        msg.body = "Seu código de recuperacao de senha é: " + code
        mail.send(msg)

     

        return {'data': 'success', 'code': 200}, 200
    return {'data':'user not found', 'code': 404}, 404 # or 204
    
@app.route("/change_password", methods=['POST'])
def change_password():
    content = request.json
    code = content["code"]
    new_password = content["new_password"]

    forgotPassword = ForgotPasswordModel.find_by_code(code)

    if forgotPassword:
       
        a = datetime.now()
        b =  forgotPassword.created_on
        
        c = a-b 
        
        minutes = c.seconds / 60

        if (minutes <= 5): 
            user = UserModel.find_user_by_id(forgotPassword.user_id)
            passwordHashad = generate_password_hash(new_password)

            user.update_user(user.id, user.email, passwordHashad, user.name)
            user.save_user()
        else: 
            return {'data':'code invalid', 'code': 400}, 400

        return {'data': 'success', 'code': 200}, 200
        
    return {'data':'code not found', 'code': 404}, 404 # or 204
    



@app.before_first_request
def create_database():
    database.create_all()

api.add_resource(Schemas, '/schemas')
api.add_resource(Schema, '/schema/<int:id>')


api.add_resource(TypesDevice, '/types_device')
api.add_resource(TypeDevice, '/types_device/<int:id>')

api.add_resource(Brands, '/brands')
api.add_resource(Brand, '/brand/<int:id>')


api.add_resource(Models, '/models')
api.add_resource(Model, '/model/<int:id>')


api.add_resource(Users, '/users')
api.add_resource(User, '/users/<int:id>')
api.add_resource(UserSession, '/login')





if __name__ == '__main__':
    from sql_alchemy import database
    database.init_app(app)
    app.run(debug=True)