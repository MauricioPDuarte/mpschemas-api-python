from flask import Flask, make_response, jsonify, request
from schemas import Schemas;
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# conexão com mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Master123@localhost/mpschemas?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



api = Api(app)

db = SQLAlchemy()
db.init_app(app)


@app.route("/schemas", methods=['GET'])
def get_schemas():
    return make_response(
        jsonify(
            message='success',
            data=Schemas
        ),
    )

@app.route("/schemas", methods=['POST'])
def create_schema():
    schema = request.json
    Schemas.append(schema);
    return make_response(
        jsonify(
            message='success',
            data=schema
        ),
    )


with app.app_context(): 
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)