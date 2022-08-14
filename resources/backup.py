from flask_restful import Resource
from pymongo import MongoClient
from os import environ
from bson.json_util import dumps


class Backup(Resource):
    def __init__(self):
        uri = "mongodb+srv://{0}:{1}@{2}/{3}?retryWrites=true&w=majority".format(
            environ.get("DB_USERNAME"),
            environ.get("DB_PASSWORD"),
            environ.get("DB_URL"),
            environ.get("DB_NAME"),
        )
        client = MongoClient(uri)
        db = client[environ.get("DB_NAME")]
        self.resource_service = db["resources"]
        self.backup_service = db["backups"]

    def post(self, resource_uuid):
        cursor = list(self.resource_service.find())
        print(dumps(cursor))
        return ''
