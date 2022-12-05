from flask import Flask, make_response, jsonify, request, send_from_directory
from flask_restful import Api


from flask_jwt_extended import JWTManager
from resources.brand import Brand, Brands
from resources.model import Model, Models
from resources.schema import Schema, Schemas
from resources.type_device import TypeDevice, TypesDevice
from flask_cors import CORS, cross_origin
from flask_mail import Mail

from resources.users import User, Users
from resources.users_session import UserSession

UPLOAD_FOLDER = 'assets/uploads'



app = Flask(__name__)
api = Api(app)
cors = CORS(app)
jwt = JWTManager(app)
mail = Mail(app)

# Configs
app.config['JSON_SORT_KEYS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/mpschemas?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'mpschemas2022trabalhoaulafacul'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'mpschemas@gmail.com'
app.config['MAIL_PASSWORD'] = 'mpschemas2022'




@app.route("/files/<path:path>")
def get_file(path):
    """Download a file."""
    return send_from_directory(UPLOAD_FOLDER, path, as_attachment=True)



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