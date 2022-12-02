from flask_restful import Resource, reqparse

from models.type_device import TypeDeviceModel

class TypesDevice(Resource):
    def get(self):
        return {'data': [device.json() for device in TypeDeviceModel.query.all()], 'code': 200}

class TypeDevice(Resource):
    minha_requisicao = reqparse.RequestParser()
    minha_requisicao.add_argument('name', type=str, required=True, help='name is required')

    def get(self, id):
        device = TypeDeviceModel.find_type_device_by_id(id)
        if device:
            return {'data':device.json(), 'code': 200 }, 200
        return {'message':'Type device not found', 'code': 404}, 404

    def post(self, id):
        dados = TypeDevice.minha_requisicao.parse_args()
        new_device = TypeDeviceModel(**dados)

        exists = new_device.find_type_device_by_name(dados.name)
        if exists:
              return {'data': 'ALREADY_EXISTS', 'code': 400 }, 400
        
        try:
            new_device.save_type_device()
            return {'data': 'Success', 'code': 201}, 201
        except:
            return {'message':'An internal error ocurred.', 'code':  500}, 500

    def put(self, id):
        dados = TypeDevice.minha_requisicao.parse_args()
        device = TypeDeviceModel.find_type_device_by_id(id)
        if device:
            exists = device.find_type_device_by_name(dados.name)
            if exists:
                return {'data': 'ALREADY_EXISTS', 'code': 400 }, 400

            device.update_type_device(**dados)
            device.save_type_device()
            return {'data': device.json(), 'code': 200 }, 200

        return {'data':'Type device not found', 'code': 404}, 404

 
    def delete(self, id):
        device = TypeDeviceModel.find_type_device_by_id(id)
        if device:
            device.delete_type_device()
            return {'data' : 'Type device deleted', 'code': 200}, 200
        return {'data' : 'Type device not founded', 'code': 404}, 404