import uuid
from db import stores,db
from flask import request
from models import StoreModel
from schemas import StoreSchema
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError,IntegrityError



blp = Blueprint("stores",__name__,description="Operations on stores")

@blp.route("/stores/<string:store_id>")
class Store(MethodView):
    @blp.response(200,StoreSchema)
    def get(self,store_id):
        item = StoreModel.query.get_or_404(store_id)
        return item

    def delete(self,store_id):
        item = StoreModel.query.get_or_404(store_id)
        raise NotImplementedError("deleting a store is not implemented")

@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200,StoreSchema)
    def get(self):
        return {"stores":list(stores.values())}

    @blp.arguments(StoreSchema)
    @blp.response(201,StoreSchema)
    def post(self,store_data):
        new_store = StoreModel(**store_data)
        try:
            db.session.add(new_store)
            db.session.commit()
        except IntegrityError:
            abort(400,message="A store with that name already exists")
        except SQLAlchemyError:
            abort(500,message="An error occurred while creating store")
        
        return new_store