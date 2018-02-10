from flask_restful import Resource, abort, fields, marshal_with, reqparse, Api
from flask import request
from app.api import status
from app import db
from sqlalchemy.exc import SQLAlchemyError
from app.api import api_api
from app import models

class Product(Resource):
    def get(self, id):
        product = models.Product.query.get_or_404(id)
        return product.to_json()
api_api.add_resource(Product, '/product/<int:id>')

class Silicon(Resource):
    def get(self, id):
        silicon = models.Silicon.query.get_or_404(id)
        return silicon.to_json()
api_api.add_resource(Silicon, '/silicon/<int:id>')

class Sample(Resource):
    def get(self, id):
        sample = models.Sample.query.get_or_404(id)
        return sample.to_json()
api_api.add_resource(Sample, '/sample/<int:id>')

class HardwareRevision(Resource):
    def get(self, id):
        hwrev = models.HardwareRevision.query.get_or_404(id)
        return hwrev.to_json()
api_api.add_resource(HardwareRevision, '/hardwarerevision/<int:id>')

class Test(Resource):
    def get(self, id):
        test = models.Test.query.get_or_404(id)
        return test.to_json()
api_api.add_resource(Test, '/test/<int:id>')

class TestID(Resource):
    def get(self, id):
        testid = models.TestID.query.get_or_404(id)
        return testid.to_json()
api_api.add_resource(TestID, '/testid/<int:id>')

class TestIDList(Resource):
    def get(self):
        #TODO
        return {"TestID" : "List Not Here"}

    def post(self):
        request_dict = request.get_json()
        print("----"*4)
        print(request_dict)
        print("----"*4)
        return models.TestID.from_json(request_dict)
api_api.add_resource(TestIDList, '/testid')

class TestRow(Resource):
    def get(self, id):
        tr = models.TestRow.query.get_or_404(id)
        return tr.to_json()
api_api.add_resource(TestRow, '/testrow/<int:id>')

class TestRowList(Resource):
    def post(self):
        request_dict = request.get_json()
        return models.TestRow.from_json(request_dict)
api_api.add_resource(TestRowList, '/testrow')

class TestData(Resource):
    def get(self, id):
        td = models.TestData.query.get_or_404(id)
        return td.to_json()
api_api.add_resource(TestData, '/testdata/<int:id>')

class TestDataList(Resource):
    def post(self):
        request_dict = request.get_json()
        return models.TestData.from_json(request_dict)
api_api.add_resource(TestDataList, '/testdata')

