from flask import g
from pymongo import MongoClient
from os import environ


def get_service(service: str):
    if g.get("db") is not None:
        return g.get("db")[service]
    uri = "mongodb+srv://{0}:{1}@{2}/{3}?retryWrites=true&w=majority".format(
        environ.get("DB_USERNAME"),
        environ.get("DB_PASSWORD"),
        environ.get("DB_URL"),
        environ.get("DB_NAME"),
    )
    client = MongoClient(uri)
    db = client[environ.get("DB_NAME")]
    g.db = db
    return db[service]
