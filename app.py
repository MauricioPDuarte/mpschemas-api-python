from flask import Flask, make_response, jsonify, request
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.brand import Brand, Brands
from resources.schema import Schemas
from resources.type_device import TypeDevice, TypesDevice
from flask_cors import CORS, cross_origin




app = Flask(__name__)
api = Api(app)
cors = CORS(app)
jwt = JWTManager(app)

# Configs
app.config['JSON_SORT_KEYS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/mpschemas?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'mpschemas2022trabalhoaulafacul'


@app.before_first_request
def create_database():
    database.create_all()

api.add_resource(Schemas, '/schemas')

api.add_resource(TypesDevice, '/types_device')
api.add_resource(TypeDevice, '/types_device/<int:id>')

api.add_resource(Brands, '/brands')
api.add_resource(Brand, '/brands')

if __name__ == '__main__':
    from sql_alchemy import database
    database.init_app(app)
    app.run(debug=True)