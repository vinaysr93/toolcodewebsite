
import os
from flask import Flask
from database import db
from config import LocalDevelopmentConfig
from flask_restful import Resource, Api


def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)

    app.app_context().push()

    return app


app = create_app()

from controllers import *

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)