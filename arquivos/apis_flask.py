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

""" 

APLICAÇÃO SEM UTILIZAR OS Blueprints

@app.post('/stores')
def create_stores():
    store_data = request.get_json()
    if "name" not in store_data:
        abort(404,message="Name not included")
    
    for store in stores.values():
        if store_data["name"] == store["name"]:
            abort(404,message="Store already exists")
            
    store_id = uuid.uuid4().hex
    new_store = {**store_data,"id":store_id}
    stores[store_id] = new_store
    return new_store, 201
        
@app.get('/stores')
def get_stores():
    return {"stores":stores}

@app.get('/stores/list')
def get_stores_list():
    return {"stores":list(stores.values())}

@app.get('/stores/items')
def get_items_list():
    return {"stores":list(items.values())}
    
@app.get("/stores/<string:store_id>")
def get_store_by_id(store_id):
    try:
        return stores[store_id]
    except:
        abort(404,message="store not found")

@app.get("/stores/<string:name>")
def get_store(name):
    for store in stores:
        if store["name"] == name:
            return store
        
    abort(404,message="store not found")

@app.get("/stores/<string:name>/item_list")
def get_items_array(name):
    for store in stores:
        if store["name"] == name:
            return store["items"]
        
    abort(404,message="item not found")

@app.delete("/store/<string:store_id>")
def delete_item(store_id):
    try:
        del stores[store_id]
        return {"message": "Store deleted successfully"}
    except KeyError:
        abort(404,message="Store not Found")

@app.post("/item")
def create_item():
    item_data = request.get_json()
    if (
        "price" not in item_data or 
        "store_id" not in item_data or
        "name" not in item_data
        ):
        abort(404,message="store not found")#mesma coisa de return {"message":"store not found"},404

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

@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except:
        abort(404,message="item not found")

@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message": "Item deleted successfully"}
    except KeyError:
        abort(404,message="Item not Found")

@app.put("/item/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()
    if "price" not in item_data or "name" not in item_data:
        abort(400,"Bad request ensure 'price' and 'name' are included in the json payload")

    try:
        item = items[item_id]
        item |= item_data

        return item
    except KeyError:
        abort(404,message="item not found")

@app.get("/item")
def get_all_items():
    return {"items":list(items.values())}

"""