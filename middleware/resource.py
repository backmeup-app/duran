from functools import wraps
from utilities.service import get_service


def resource_middleware(method):
    @wraps(method)
    def middleware(*args, **kwargs):
        resource_uuid = kwargs.get("resource_uuid")
        resource_service = get_service("resources")
        resource = resource_service.find_one({"uuid": resource_uuid})

        if resource is None:
            return {
                "message": "resource with uuid {0} does not exist".format(resource_uuid)
            }, 404

        return method(*args, **kwargs)

    return middleware
