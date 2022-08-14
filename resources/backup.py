from flask_restful import Resource 

class Backup(Resource):
    def post(self, resource_uuid):
        print(';elel')