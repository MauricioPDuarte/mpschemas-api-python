from flask_restful import Resource, reqparse
from models.brand import BrandModel

from models.model import ModelModel
from resources.brand import Brand


class Models(Resource):
    def get(self):
        return {'data': [model.json() for model in ModelModel.query.join(BrandModel).all()], 'code': 200}, 200

class Model(Resource):
    minha_requisicao = reqparse.RequestParser()
    minha_requisicao.add_argument('name', type=str, required=True, help='name is required')
    minha_requisicao.add_argument('brand_id', type=int, required=True, help='Brand is required')
   

    def get(self, id):
        device = ModelModel.find_by_id(id)
        if device:
            return {'data': device.json(), 'code': 200}, 200
        return {'data':'item not found', 'code': 404}, 404 # or 204

    def post(self, id):
        dados = Model.minha_requisicao.parse_args()
        new_item = ModelModel(**dados)

        
        try:
            brand = BrandModel.find_brand_by_id(new_item.brand_id)

            if not brand:
                return {'data':'brand not found', 'code': 404}, 404 # or 204

            new_item.save()
            return {'data': 'success', 'code': 200}, 200
        except:
            return {'data':'An internal error ocurred.', 'code': 500}, 500

    def put(self, id):
        dados = Model.minha_requisicao.parse_args()
        item = ModelModel.find_by_id(id)

        if item:
            brand = BrandModel.find_brand_by_id(dados.brand_id)
            
            if not brand:
                return {'data':'brand not found', 'code': 404}, 404 # or 204

            item.update(**dados)
            item.save()
            return item.json(), 200
        else: 
          return {'data': 'item not founded', 'code': 404}, 404


    def delete(self, id):
        device = ModelModel.find_by_id(id)
        if device:
            device.delete()
            return {'data' : 'item deleted', 'code': 200}, 200
        return {'data' : 'item not founded', 'code': 404}, 404