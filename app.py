from flask import Flask, make_response, jsonify, request
from schemas import Schemas;

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

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
