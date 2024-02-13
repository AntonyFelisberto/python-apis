import uuid
from db import db
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from flask_smorest import Blueprint, abort
from schemas import TagSchema,TagAndItemSchema
from models import TagModel,StoreModel,ItemModel

blp = Blueprint("Tags",__name__,description="Operations on tags")

@blp.route("/store/<int:store_id>/tag")
class TagsInStore(MethodView):
    @blp.response(200,TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()
    
    @blp.arguments(TagModel)
    @blp.response(201,TagSchema)
    def post(self,tag_data,store_id):
        if TagModel.query.filter(TagModel.store_id == store_id, TagModel.name == tag_data["name"]).first():
            abort(400,message="tag already exists")

        tag = TagModel(**tag_data,store_id=store_id)
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500,message=str(e))

        return tag
    
@blp.route("/item/<int:item_id>/tags/<int:tag_id>")
class LinkToTagItem(MethodView):
    @blp.response(201,TagSchema)
    def post(self,item_id,tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)
        
        item.tags.append(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message="An error ocurred while inserting the tag.")

        return tag
    
    @blp.response(200,TagAndItemSchema)
    def delete(self,item_id,tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)
        
        item.tags.remove(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message="An error ocurred while deleting the tag.")

        return {"message":"Item removed from tag","item":item,"tag":tag}

@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):
    @blp.response(200,TagSchema)
    def get(self,tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag
    
    @blp.response(202,description="delete a tag if item is tagged with it",example={"message":"tag deleted"})
    @blp.alt_response(404,description="Tag not found")
    @blp.alt_response(400,description="returned if the tag is assigned to one or more items in this case, the tag is not deleted")
    def delete(self,tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message":"tag deleted"}

        abort(400,message="could not delete tag, make sure tag is not associated with any items, then try again")