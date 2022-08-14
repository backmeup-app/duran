from flask import Flask
from flask_restful import Api, Resource
from resources.backup import Backup
from utilities.env import load_env
from os import environ

# Loading relevant environment variables
load_env()

app = Flask(__name__)
api = Api(app)

api.add_resource(Backup, "/<resource_uuid>")

if __name__ == "__main__":
    port = int(environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
