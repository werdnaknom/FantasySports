from flask_restful import Resource
import request
from app.api import status
from app import db
from sqlalchemy.exc import SQLAlchemyError

class Test(Resource):
    def get(self, id):
        return {"TestID" : "Test1234"}

    def post(self):
        return {"Post" : "Post"}

class TestData(Resource):
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

