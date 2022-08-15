from flask import request
from flask_restful import Resource, reqparse
from bson.json_util import dumps
from utilities.service import get_service
from utilities.resource import validate_resource
from utilities.upload import upload_to_cloudinary
from middleware.resource import resource_middleware


class Backup(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            "backup", location="files", required=True, help="backup is not provided"
        )
        self.method_decorators = [resource_middleware]
        self.resource_service = get_service("resources")
        self.service_service = get_service("services")
        self.backup_service = get_service("backups")
        self.user_service = get_service("users")

    def post(self, resource_uuid):
        self.parser.parse_args()
        resource = self.resource_service.find_one({"uuid": resource_uuid})
        service = self.service_service.find_one({"_id": resource.get("service")})

        if not validate_resource(resource, self.backup_service):
            return {
                "message": "resource with uuid {0} has been backed up already today".format(
                    resource_uuid
                )
            }

        upload_response = upload_to_cloudinary(
            request.files.get("backup"), resource, service
        )

        if upload_response is None:
            return {
                "message": "backup operation failed"
            }
        print(upload_response)
        return ""
