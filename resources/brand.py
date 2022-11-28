from flask_restful import Resource, reqparse
from models.brand import BrandModel


class Brands(Resource):
    def get(self):
        return {'brands': [device.json() for device in BrandModel.query.all()]}

class Brand(Resource):
    minha_requisicao = reqparse.RequestParser()
    minha_requisicao.add_argument('name', type=str, required=True, help='name is required')

    def get(self, id):
        device = BrandModel.find_brand_by_id(id)
        if device:
            return device.json()
        return {'message':'device not found'}, 200 # or 204

    def post(self):
        dados = Brand.minha_requisicao.parse_args()
        new_device = BrandModel(**dados)
        
        try:
            new_device.save_brand()
        except:
            return {'message':'An internal error ocurred.'}, 500

    def put(self, id):
        dados = Brand.minha_requisicao.parse_args()
        device = BrandModel.find_device_by_id(id)
        if device:
            device.update_device(**dados)
            device.save_device()
            return device.json(), 200

        device_id = BrandModel.find_last_device()
        new_device = BrandModel(device_id, **dados)
        new_device.save_brand()
        return new_device.json(), 201

    def delete(self, id):
        device = BrandModel.find_brand_by_id(id)
        if device:
            device.delete_brand()
            return {'message' : 'Brand deleted.'}
        return {'message' : 'Brand not founded'}, 204