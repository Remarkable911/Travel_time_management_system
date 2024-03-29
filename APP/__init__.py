#初始化

from flask import Flask
from .views import blue
def create_app():
    app=Flask(__name__)
    app.register_blueprint(blueprint=blue)
    return app