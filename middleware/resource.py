from flask import request
from functools import wraps
from utilities.backup import is_backed_up_today
from utilities.date import get_timestamp
from utilities.mail import Mail
from utilities.service import get_service


def resource_middleware(method):
    @wraps(method)
    def middleware(*args, **kwargs):
        resource_uuid = kwargs.get("resource_uuid")
        resource_service = get_service("resources")
        service_service = get_service("services")
        user_service = get_service("users")
        resource = resource_service.find_one({"uuid": resource_uuid})

        if resource is None:
            return {
                "message": "resource with uuid {0} does not exist".format(resource_uuid)
            }, 404

        auth_header = request.headers.get("Authorization")
        service = service_service.find_one({"_id": resource["service"]})
        user = user_service.find_one({"_id": service["user"]})

        if auth_header is None or len(auth_header.split(" ")) != 2:
            is_authorized = False
            key = None
        else:
            key = auth_header.split(" ")[1]
            api_keys = list(map(lambda key: key["key"], service["api_keys"]))
            is_authorized = key in api_keys

        if not is_authorized:
            if service.get("notifications").get("events").get("BR_WRONG_CREDENTIALS"):
                mail = Mail(
                    user["email"],
                    "{0} - Unauthorized Backup Request".format(
                        resource["name"].capitalize()
                    ),
                    "backup_request_unauthorized.html",
                    resource=resource,
                    service=service,
                    user=user,
                    timestamp=get_timestamp(),
                    key=key,
                )
                mail.send()
            return {
                "message": "unauthorized",
            }, 401

        # if not is_backed_up_today(resource, get_service("backups")):
        #     return {
        #         "message": "resource has been backed up today"
        #     }, 400

        return method(*args, **kwargs)

    return middleware
