import os
from flask_restful import Resource, reqparse
from models.brand import BrandModel
from models.model import ModelModel
from models.schama import SchemaModel
from flask import current_app
import uuid

from models.type_device import TypeDeviceModel
from models.user import UserModel
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from utils import allowed_file


class Schemas(Resource):
      def get(self):
        return {'data' : [schema.json() for schema in SchemaModel.query.all()], 'code': 200}, 200


class Schema(Resource):
  minha_requisicao = reqparse.RequestParser()
  minha_requisicao.add_argument('brand_id', type=int, location='form', required=True, help="brand is required",)
  minha_requisicao.add_argument('model_id', type=int, required=True, location='form', help="model is required")
  minha_requisicao.add_argument('type_device_id', type=int, required=True, location='form', help="type device is required")
  minha_requisicao.add_argument('user_id', type=int, required=True, location='form', help="user is required")
  minha_requisicao.add_argument('file', type=FileStorage, location='files',  required=False)

  

  def get(self, id):
      device = SchemaModel.find_by_id(id)
      if device:
          return {'data': device.json(), 'code': 200}, 200
      return {'data':'item not found', 'code': 404}, 404 # or 204

  def post(self, id):
      dados = Schema.minha_requisicao.parse_args()

      try:
        brand = BrandModel.find_brand_by_id(dados.brand_id)

        if not brand:
            return {'data':'brand not found', 'code': 404}, 404 # or 204

        model = ModelModel.find_by_id(dados.model_id)

        if not model:
            return {'data':'model not found', 'code': 404}, 404 # or 204

        typeDevice = TypeDeviceModel.find_type_device_by_id(dados.type_device_id)

        if not typeDevice:
            return {'data':'type device not found', 'code': 404}, 404 # or 204

        user = UserModel.find_user_by_id(dados.user_id)

        if not user:
            return {'data':'user not found', 'code': 404}, 404 # or 204

        file = dados.file
        filename = None
        if file and allowed_file(file.filename):
            filename = str(uuid.uuid4()) + '-' + dados.file.filename
            path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(path)

        new_item = SchemaModel(dados.type_device_id, dados.user_id, dados.model_id, dados.brand_id, filename)

        new_item.save()
        return {'data': 'success', 'code': 200}, 200
      except Exception as e:
          print(e)
          return {'data':'An internal error ocurred.', 'code': 500}, 500

  def put(self, id):
      dados = Schema.minha_requisicao.parse_args()
      item = SchemaModel.find_by_id(id)

      if item:
          brand = BrandModel.find_brand_by_id(dados.brand_id)

          if not brand:
              return {'data':'brand not found', 'code': 404}, 404 # or 204

          model = ModelModel.find_by_id(dados.model_id)

          if not model:
              return {'data':'model not found', 'code': 404}, 404 # or 204

          typeDevice = TypeDeviceModel.find_type_device_by_id(dados.type_device_id)

          if not typeDevice:
              return {'data':'type device not found', 'code': 404}, 404 # or 204

          user = UserModel.find_user_by_id(dados.user_id)

          if not user:
              return {'data':'user not found', 'code': 404}, 404 # or 204

          filename = item.path
          if dados.file and allowed_file(dados.file.filename):
            filename = str(uuid.uuid4()) + '-' + dados.file.filename
            path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            dados.file.save(path)

            if item.path:
              oldpath = os.path.join(current_app.config['UPLOAD_FOLDER'], item.path)
              os.remove(oldpath)

          item.update(dados.type_device_id,  dados.brand_id, dados.model_id, dados.user_id, filename)
          item.save()
          return item.json(), 200
      else: 
        return {'data': 'item not founded', 'code': 404}, 404


  def delete(self, id):
      item = SchemaModel.find_by_id(id) 
      if item:
        if item.path:
            oldpath = os.path.join(current_app.config['UPLOAD_FOLDER'], item.path)
            os.remove(oldpath)

        item.delete()
        return {'data' : 'item deleted', 'code': 200}, 200

      return {'data' : 'item not founded', 'code': 404}, 404