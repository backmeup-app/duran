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
        cloudinary.uploader.upload(backup, folder=folder, public_id=uuid, resource_type='auto')
    except Exception as e:
        print(e)
        return None

    url = cloudinary.CloudinaryImage(uuid).build_url()

    return (uuid, url)
