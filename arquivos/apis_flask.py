import os
from db import db
from flask_smorest import Api
from dotenv import load_dotenv
from blocklist import BLOCKLIST
from flask import Flask,jsonify
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint

#flask run PARA RODAR O ARQUIVO, O CMD TEM QUE ESTAR APONTANDO PARA A PASTA QUE TEM O ARQUIVO
def create_app(db_url=None):
    app = Flask(__name__)
    load_dotenv()

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config['API_TITLE'] = "Stores Rest api"
    app.config["API_VERSION"] = "V1"
    app.config["OPENAPI_VERSION"]= "3.0.3"
    app.config["OPENAPI_URL_PREFIX"]= "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"]= "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"]= "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"]=db_url or os.getenv("DATABASE_URL","sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
    app.config["JWT_SECRET_KEY"] = "SHA256"
    
    db.init_app(app)

    migrate = Migrate(app,db)
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header,jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header,jwt_payload):
        return(
            jsonify(
                {"description":"token has been revoked","error":"token revoked"}
            ),
            401
        )

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        if identity == 1:
            return {"is_admin":True}
        return {"is_admin":False}

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header,jwt_payload):
        return(
            jsonify(
                {"message":"token has expired","error":"token expired"}
            ),
            401
        )
    
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header,jwt_payload):
        return(
            jsonify(
                {"message":"token not fresh","error":"token fresh required"}
            ),
            401
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return(
            jsonify(
                {"message":"Signature verification failed","error":"invalid token"}
            ),
            401
        )
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return(
            jsonify(
                {"message":"Request does not contain access token","error":"authorization token"}
            ),
            401
        )

    api = Api(app)

    with app.app_context():
        db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    return app