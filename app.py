from flask import Flask
from flask_restful import Api, Resource
from resources.backup import Backup
from utilities.env import load_env
from os import environ, path
import logging

logging.basicConfig(
    filename=str(path.join(path.dirname(__file__), "logs", "duran.log")),
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s : %(message)s",
)

# Loading relevant environment variables
load_env()

app = Flask(__name__)
api = Api(app)

api.add_resource(Backup, "/<resource_uuid>")
