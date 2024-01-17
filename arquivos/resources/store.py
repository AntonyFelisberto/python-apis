import uuid
from db import stores
from flask import request
from schemas import StoreSchema
from flask.views import MethodView
from flask_smorest import Blueprint, abort


blp = Blueprint("stores",__name__,description="Operations on stores")

@blp.route("/stores/<string:store_id>")
class Store(MethodView):
    def get(self,store_id):
        try:
            return stores[store_id]
        except:
            abort(404,message="store not found")

    def delete(self,store_id):
        try:
            del stores[store_id]
            return {"message": "Store deleted successfully"}
        except KeyError:
            abort(404,message="Store not Found")

@blp.route("/store")
class StoreList(MethodView):
    def get(self):
        return {"stores":list(stores.values())}

    @blp.arguments(StoreSchema)
    def post(self,store_data):
        for store in stores.values():
            if store_data["name"] == store["name"]:
                abort(404,message="Store already exists")
                
        store_id = uuid.uuid4().hex
        new_store = {**store_data,"id":store_id}
        stores[store_id] = new_store
        return new_store, 201