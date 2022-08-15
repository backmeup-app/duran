import cloudinary
import cloudinary.uploader
from os import environ
from uuid import uuid4


def upload_to_cloudinary(backup, resource, service):
    cloudinary.config(secure=True)
    cloudinary_folder = environ.get("CLOUDINARY_FOLDER")
    folder = "{0}/{1}/{2}".format(cloudinary_folder, service["uuid"], resource["uuid"])
    uuid = str(uuid4())

    try:
        response = cloudinary.uploader.upload(backup, folder=folder, public_id=uuid, access_mode='public', resource_type='auto')
        url = response['secure_url']
    except Exception as e:
        print(e)
        return None

    return (uuid, url)
