import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items,stores

blp = Blueprint("Items",__name__,description="Operations on stores")

@blp.route("/item/<string:item_id>")
class Item(MethodView):
    def get(self,item_id):
        try:
            return items[item_id]
        except:
            abort(404,message="item not found")

    def delete(self,item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted successfully"}
        except KeyError:
            abort(404,message="Item not Found")
    
    def put(self,item_id):
        item_data = request.get_json()
        if "price" not in item_data or "name" not in item_data:
            abort(400,"Bad request ensure 'price' and 'name' are included in the json payload")

        try:
            item = items[item_id]
            item |= item_data

            return item
        except KeyError:
            abort(404,message="item not found")

@blp.route("/item")
class Item(MethodView):
    def get(self,item_id):
        return {"items":list(items.values())}

    def post(self):
        item_data = request.get_json()
        if (
            "price" not in item_data or 
            "store_id" not in item_data or
            "name" not in item_data
            ):
            abort(404,message="store not found")    #mesma coisa de return {"message":"store not found"},404

        for item in items.values():
            if (
                item_data["name"] == item["name"] and
                item_data["store_id"] == item["store_id"]
            ):
                abort(404,message="Item already exist")

        if item_data["store_id"] not in stores:
            abort(404,message="Store not found")

        item_id=uuid.uuid4().hex
        item = {**item_data,"id":item_id}
        items[item_id]=item
        return item, 201