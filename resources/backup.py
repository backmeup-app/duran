from flask import request
from flask_restful import Resource, reqparse
from datetime import datetime
from utilities.date import get_timestamp
from utilities.service import get_service
from utilities.mail import Mail
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
        user = self.user_service.find_one({"_id": service.get("user")})

        upload_response = upload_to_cloudinary(
            request.files.get("backup"), resource, service
        )

        if upload_response is None:
            return {"message": "backup operation failed"}

        (uuid, url) = upload_response
        self.backup_service.insert_one(
            {
                "uuid": uuid,
                "resource": resource["_id"],
                "url": url,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
            }
        )

        if service.get("notifications").get("events").get("BR_SUCCESSFUL"):
            mail = Mail(
                user["email"],
                "{0} - New Backup".format(resource["name"].capitalize()),
                "backup_successful.html",
                resource=resource,
                service=service,
                user=user,
                timestamp=get_timestamp(),
            )

            mail.send()

        return ""
