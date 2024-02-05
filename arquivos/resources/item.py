import uuid
from flask import request
from models import ItemModel
from schemas import ItemSchema
from db import items,stores,db
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("Items",__name__,description="Operations on stores")

@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200,ItemSchema)
    def get(self,item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    def delete(self,item_id):
        item = ItemModel.query.get_or_404(item_id)
        raise NotImplementedError("deleting an item is not implemented")
    
    @blp.arguments(ItemSchema)
    @blp.response(200,ItemSchema)
    def put(self,item_data,item_id):
        item = ItemModel.query.get_or_404(item_id)
        raise NotImplementedError("updating an item is not implemented")

@blp.route("/item")
class Item(MethodView):
    @blp.response(200,ItemSchema(many=True))
    def get(self):
        return items.values()

    @blp.arguments(ItemSchema)
    @blp.response(201,ItemSchema)
    def post(self,item_data):
        item = ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message="Am error occurred while creating store")

        return item, 201