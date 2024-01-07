import uuid
from flask import Flask,request
from flask_smorest import abort
from db import stores,items

#flask run PARA RODAR O ARQUIVO, O CMD TEM QUE ESTAR APONTANDO PARA A PASTA QUE TEM O ARQUIVO
app = Flask(__name__)

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

@app.get("/stores/<string:name>/item_list")
def get_items_array(name):
    for store in stores:
        if store["name"] == name:
            return store["items"]
        
    abort(404,message="item not found")

@app.get("/item")
def get_all_items():
    return {"items":list(items.values())}