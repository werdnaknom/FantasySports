from flask_restful import Resource, abort, fields, marshal_with, reqparse, Api
import request
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

    def post(self):
        return {"Post" : "Post"}
api_api.add_resource(TestID, '/testid/<int:id>')

class TestRow(Resource):
    def get(self, id):
        tr = models.TestRun.query.get_or_404(id)
        return tr.to_json()
api_api.add_resource(TestRow, '/testrow/<int:id>')

class TestData(Resource):
    def get(self, id):
        td = models.TestData.query.get_or_404(id)
        return td.to_json()

    def post(self):
        request_dict = request.get_json()
        if not request_dict:
            response = {"message" : "No input data provided"}
            return response, status.HTTP_400_BAD_REQUEST
        try:
            #TODO: Database entry
            print("Hello")
        except SQLAlchemy as e:
            db.session.rollback()
            resp = jsonify({"error" : str(e)})
            return resp, status.HTTP_400_BAD_REQUEST
api_api.add_resource(TestData, '/testdata/<int:id>')

