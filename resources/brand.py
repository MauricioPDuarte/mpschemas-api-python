from flask_restful import Resource, reqparse
from models.brand import BrandModel


class Brands(Resource):
    def get(self):
        return {'data': [device.json() for device in BrandModel.query.all()], 'code': 200}, 200

class Brand(Resource):
    minha_requisicao = reqparse.RequestParser()
    minha_requisicao.add_argument('name', type=str, required=True, help='name is required')

    def get(self, id):
        device = BrandModel.find_brand_by_id(id)
        if device:
            return {'data': device.json(), 'code': 200}, 200
        return {'data':'device not found', 'code': 404}, 404 # or 204

    def post(self, id):
        dados = Brand.minha_requisicao.parse_args()
        new_device = BrandModel(**dados)
        
        try:
            new_device.save_brand()
            return {'data': 'success', 'code': 200}, 200
        except:
            return {'data':'An internal error ocurred.', 'code': 500}, 500

    def put(self, id):
        dados = Brand.minha_requisicao.parse_args()
        device = BrandModel.find_brand_by_id(id)
        if device:
            device.update_brand(**dados)
            device.save_brand()
            return device.json(), 200
        else: 
          return {'data': 'brand not founded', 'code': 404}, 404


    def delete(self, id):
        device = BrandModel.find_brand_by_id(id)
        if device:
            device.delete_brand()
            return {'data' : 'brand deleted', 'code': 200}, 200
        return {'data' : 'brand not founded', 'code': 404}, 404