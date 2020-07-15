from db import db

# db is SQLALchemy. Passing the db.Model to the ItemModel, tells SQLAlchemy
# that this model will be accessing the database file and do database operations.
# The table property tells SQLAlchemy that this model will be accessing that table.
# The other properties represent each column in that table.
class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    store_id = db.Column(db.Integer, db.ForeignKey('stores.store_id'))
    # The store property is a relationship between the ItemModel and the StoreModel.
    # When a store object is created, it will add the items with the store id to the
    # items property of the store object.
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    # The json method creates a dictionary with the item information.
    def json(self):
        return {'name': self.name, 'price': self.price, 'Store': self.store_id}

    # The find by name class method takes in a name. Then  give the name
    # to SQLAlchemy to create a query by filtering using the name, and
    # returning the first result.
    # If a result is found by SQLAlchemy then it returns a ItemModel object
    # with all the item information, else it returns None.
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    # This method tells SQLAlchemy to save the store to the database.
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # This method tells SQLAlchemy to delete the store from the database.
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
