from flask_restful import Resource, reqparse

from models.schama import SchemaModel


class Schemas(Resource):
      def get(self):
        return {'schemas' : [schema.json() for schema in SchemaModel.query.all()]}


class Schema(Resource):
    minha_requisicao = reqparse.RequestParser()
    minha_requisicao.add_argument('name', type=str, required=True, help="name is required")
