from flask_restful import Resource
from models.store import StoreModel

# Store is used as a Resource from flask_restful.
# Flask restful resources are able to receive CRUD requests using
# methods within them.
class Store(Resource):

    existing = {'message': 'This store already exists'}
    created = {'message': 'The store was successfully created'}
    deleted = {'message': 'The store was successfully deleted'}
    not_found = {'message': 'This store does not exists'}
    error = {'message': 'There was a server error while processing your request'}

    # Give the name to the StoreModel find by name class method. This method creates
    # an object with the store information if the store is found, else it returns None.
    # If the store object is generated, return the information of the store, by using
    # the json method in the store to create a json representation of the object.
    # If the store was not found return the message and 404 code
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json, 200
        return Store.not_found, 404

    # If the Store Model find by name class method returns an object, then
    # return the existing message and 400 code.
    # If Store Model find by name class method returns None.
    # Create a store object with the name provided, and try to use the store save to
    # db method to save to databse using SQLAlchemy. If an error occurs during
    # this process then return server error, else return store created and 201.
    def post(self, name):
        if StoreModel.find_by_name(name):
            return Store.existing, 400
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            Store.error, 500
        return Store.created, 201

    # store is the result from the find by name class method. If an object is returned
    # then use the object's delete from db method to delete it from the database.
    # If and error occurs then return server error, else return deleted message.
    # If store model find by name returned None, then return store not found 404.
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            try:
                store.delete_from_db()
            except:
                Store.error, 500
            return Store.deleted, 200
        return Store.not_found, 404


# StoreList is another Resource which returns a list of stores in json format.
class StoreList(Resource):
    # call the StoreModel SQLAlchemy method query all to retrieve all the stores
    # in the database. This returns a list of store objects containing the store information
    # and items. Then we use list comprehension to call the json method in each store
    # object and create a list of stores in json format. Then return a dictionary
    # with the list of stores.
    def get(self):
        stores = [store.json() for store in StoreModel.query.all()]
        return {'stores': stores}

