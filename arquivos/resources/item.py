import uuid
from db import db
from flask import request
from models import ItemModel
from schemas import ItemSchema
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from flask_smorest import Blueprint, abort

blp = Blueprint("Items",__name__,description="Operations on stores")

@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200,ItemSchema)
    def get(self,item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    def delete(self,item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted successfully"}
    
    @blp.arguments(ItemSchema)
    @blp.response(200,ItemSchema)
    def put(self,item_data,item_id):
        item = ItemModel.query.get(item_id)
        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(id=item_id,**item_data)

        db.session.add(item)
        db.session.commit()

        return item

@blp.route("/item")
class Item(MethodView):
    @blp.response(200,ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

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