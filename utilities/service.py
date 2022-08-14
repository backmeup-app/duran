from pymongo import MongoClient
from os import environ


def get_service(service: str):
    uri = "mongodb+srv://{0}:{1}@{2}/{3}?retryWrites=true&w=majority".format(
        environ.get("DB_USERNAME"),
        environ.get("DB_PASSWORD"),
        environ.get("DB_URL"),
        environ.get("DB_NAME"),
    )
    client = MongoClient(uri)
    db = client[environ.get("DB_NAME")]
    return db[service]
