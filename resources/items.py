from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.items import ItemModel


# Items is a flask_restful Resource which returns a list of stores in json format.
class Items(Resource):
    # call the ItemModel SQLAlchemy method query all to retrieve all the items
    # in the database. This returns a list of item objects containing the item
    # information. Then we use list comprehension to call the json method in each
    # item object and create a list of stores in json format. Then return a
    # dictionary with the list of items.
    def get(self):
        items = [item.json() for item in ItemModel.query.all()]
        return {'items': items}, 201


# Item is used as a Resource from flask_restful.
# Flask restful resources are able to receive CRUD requests using
# methods within them.
class Item(Resource):
    # reqparse is used to validate the data provided by the request.
    # In this case it will format the data to only contain the arguments
    # we want, which are username and password. Anything else gets discarded
    # from the data.
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This field is required.')
    parser.add_argument('store_id',
                        type=float,
                        required=True,
                        help='Every item needs a store id.')
    not_found = {'message': 'The item provided was not found.'}
    existing = {'message': 'That item already exists in inventory.'}
    created = 'Item has been added to the inventory successfully.'
    deleted = {'message': 'The item has been deleted from the inventory.'}
    updated = 'The item has been updated successfully.'
    error = {'message': 'There was a server error processing the item'}

    # jwt required is a wrapper which tells jwt that in order to access
    # this methods request, the user needs to be validated.
    @jwt_required()
    # Give the name to the ItemModel find by name class method. This method creates
    # an object with the store information if the item is found, else it returns None.
    # If the item object is generated, return the information of the item, by using
    # the json method in the item to create a json representation of the object.
    # If the item was not found return the message and 404 code
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200
        return Item.not_found, 404

    # If the Item Model find by name class method returns an object, then
    # return the existing message and 400 code.
    # If ItemModel find by name class method returns None. grab the validated
    # data from the parser and create a item object with the name provided
    # and the packed data.
    # Try to use the item save to db method to save to database using SQLAlchemy.
    # If an error occurs during this process then return server error,
    # else return store created and 201.
    def post(self, name):
        if ItemModel.find_by_name(name):
            return Item.existing, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return Item.error, 500
        return {'message': Item.created,
                'item': item.json()}, 201

    # item is the result from the find by name class method. If an object is returned
    # then use the object's delete from db method to delete it from the database.
    # If and error occurs then return server error, else return deleted message.
    # If item model find by name returned None, then return item not found 404.
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return Item.deleted, 200
        return Item.not_found, 404

    # Grab teh validated arguments and store them in data.
    # Use the ItemModel find by name to return the object or None.
    # If and object is returned, set the action to updated, code to 200, and
    # unpack data into the item price and the item store id.
    # If None is returned, set action to created, code to 201, and create
    # an ItemModel object with the name provided and validated data.
    # Regardless if the item was found or created, use the item save to db method
    # to write to the database using SQLAlchemy. If an error occurs show server
    # error message and return 500, else return a message withe the action and code.
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item:
            action = 'updated'
            code = 200
            item.price, item.store_id = data['price'], data['store_id']
        else:
            action = 'created'
            code = 201
            item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return Item.error, 500
        return {'message': f"Item has been {action}.",
                'item': item.json()}, code
