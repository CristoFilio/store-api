from db import db

# db is SQLALchemy. Passing the db.Model to the StoreModel, tells SQLAlchemy
# that this model will be accessing the database file and do database operations.
# The table property tells SQLAlchemy that this model will be accessing that table.
# The other properties represent each column in that table.
class StoreModel(db.Model):
    __tablename__ = 'stores'

    store_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    # The items property is a relationship between the ItemModel and the StoreModel.
    # The items  are created with a store id in them. SQLALchemy looks for the items
    # with the store id and creates a relationship. The lazy property tells SQLAlchemy
    # to only create this relationship when the store object is requested.
    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    # call the StoreModel SQLAlchemy method query all to retrieve all the items
    # in the database assigned to the store. This returns a list of item objects
    # containing the item information. Then we use list comprehension to call the
    # json method in each item object and create a list of items in json format.
    # Then return a dictionary with the store name and a list of its items.
    def json(self):
        store_items = [item.json() for item in self.items.all()]
        return {'name': self.name, 'items': store_items}

    # The find by name class method takes in a name. Then  give the name
    # to SQLAlchemy to create a query by filtering using the name, and
    # returning the first result.
    # If a result is found by SQLAlchemy then it returns a StoreModel object
    # with all the store information, else it returns None.
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()  # SELECT * FROM items WHERE name=name

    # This method tells SQLAlchemy to save the store to the database.
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # This method tells SQLAlchemy to delete the store from the database.
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
