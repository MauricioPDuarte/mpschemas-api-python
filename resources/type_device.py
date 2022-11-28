from flask_restful import Resource, reqparse

from models.type_device import TypeDeviceModel

class TypesDevice(Resource):
    def get(self):
        return {'types_device': [device.json() for device in TypeDeviceModel.query.all()]}

class TypeDevice(Resource):
    minha_requisicao = reqparse.RequestParser()
    minha_requisicao.add_argument('name', type=str, required=True, help='name is required')

    def get(self, id):
        device = TypeDeviceModel.find_type_device_by_id(id)
        if device:
            return device.json()
        return {'message':'device not found'}, 200 # or 204

    def post(self):
        dados = TypeDevice.minha_requisicao.parse_args()
        new_device = TypeDeviceModel(**dados)
        
        try:
            new_device.save_type_device()
        except:
            return {'message':'An internal error ocurred.'}, 500

    def put(self, id):
        dados = TypeDevice.minha_requisicao.parse_args()
        device = TypeDeviceModel.find_device_by_id(id)
        if device:
            device.update_device(**dados)
            device.save_device()
            return device.json(), 200

        device_id = TypeDeviceModel.find_last_device()
        new_device = TypeDeviceModel(device_id, **dados)
        new_device.save_type_device()
        return new_device.json(), 201

    def delete(self, id):
        device = TypeDeviceModel.find_type_device_by_id(id)
        if device:
            device.delete_type_device()
            return {'message' : 'Device deleted.'}
        return {'message' : 'device not founded'}, 204