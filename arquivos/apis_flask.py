import uuid
from db import stores,items
from flask import Flask,request
from flask_smorest import abort,Api
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint

#flask run PARA RODAR O ARQUIVO, O CMD TEM QUE ESTAR APONTANDO PARA A PASTA QUE TEM O ARQUIVO
app = Flask(__name__)

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config['API_TITLE'] = "Stores Rest api"
app.config["API_VERSION"] = "V1"
app.config["OPENAPI_VERSION"]= "3.0.3"
app.config["OPENAPI_URL_PREFIX"]= "/"
app.config["OPENAPI_SWAGGER_UI_PATH"]= "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"]= "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)
api.register_blueprint(ItemBlueprint)
api.register_blueprint(StoreBlueprint)