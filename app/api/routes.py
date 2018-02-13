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

class AddSample(Resource):
    def post(self):
        request_dict = request.get_json()
        return models.Sample.from_json(request_dict)
api_api.add_resource(AddSample, '/sample/')

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

class AddTestID(Resource):
    def get(self):
        #TODO
        return {"TestID" : "List Not Here"}

    def post(self):
        request_dict = request.get_json()
        return models.TestID.from_json(request_dict)
api_api.add_resource(AddTestID, '/testid')

class TestRow(Resource):
    def get(self, id):
        tr = models.TestRow.query.get_or_404(id)
        return tr.to_json()
api_api.add_resource(TestRow, '/testrow/<int:id>')

class AddTestRow(Resource):
    def post(self):
        request_dict = request.get_json()
        return models.TestRow.from_json(request_dict)
api_api.add_resource(AddTestRow, '/testrow')

class TestData(Resource):
    def get(self, id):
        td = models.TestData.query.get_or_404(id)
        return td.to_json()
api_api.add_resource(TestData, '/testdata/<int:id>')

class AddTestData(Resource):
    def post(self):
        request_dict = request.get_json()
        return models.TestData.from_json(request_dict)
api_api.add_resource(AddTestData, '/testdata')

class TestInformation(Resource):
    def post(self):
        request_dict = request.get_json()
        product = models.Product.query.filter_by(baseSerial=
                                           request_dict['baseSerial']).all()
        if len(product) == 0:
            response = {"message" : "Product doesn't exist"}
            return response, status.HTTP_400_BAD_REQUEST
        else:
            hwrev_number = request_dict['hwrev']
            hwrev = [hwrev for hwrev in product.hw_revisions.all() if
                     hwrev.reworkNumber == hwrev_number]
            if len(hwrev) == 0:
                response = {"message" : "Hardware Revision doesn't exist"}
                return response, status.HTTP_400_BAD_REQUEST
                product_id = product[0].id
                hwrev_id = hwrev[0].id
                serial = request_dict['serial']
                samples = product.samples.filter_by(serial=serial).all()
                sampleList = [sample.id for sample in samples]
                if len(samples) > 0:
                    sample_hw = models.SampleHardware.query.filter_by(
                        hw_revision_id = hwrev_id).all()
                    sample = [sample for sample in sample_hw if
                              sample.sample_id in sampleList]
                if not sample:
                    sample_dict = {
                        "serial" : serial,
                        "product_id" : product_id,
                        "hardware_revision_id" : hwrev_id,
                    }
                    return models.Sample.from_json(sample_dict)
                else:
                    return 1234
