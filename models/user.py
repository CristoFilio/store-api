from db import db

# db is SQLALchemy. Passing the db.Model to the UserModel, tells SQLAlchemy
# that this model will be accessing the database file and do database operations.
# The table property tells SQLAlchemy that this model will be accessing that table.
# The other properties represent each column in that table.
class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    access = db.Column(db.Integer)

    # The user model contains needs to be provided a username, password, and access.
    # The user id is created by the database using primary keys.
    def __init__(self, username, password, access):
        self.username = username
        self.password = password
        self.access = access

    # The find user class method takes in either username or id.
    # The username is provided by the authenticate function.
    # If a username is provided then use SQLAlchemy to create a query
    # by filtering using the username, and returning the first result.
    # If a result is found by SQLAlchemy then it returns a UserModel object
    # with all the user information, else it returns None.
    # The identity function provides the find user method with the id. The
    # rest of the process is the same as if the user is provided.
    @classmethod
    def find_user(cls, username=None, _id=None):
        if username:
            return cls.query.filter_by(username=username).first()
        if _id:
            return cls.query.filter_by(id=_id).first()

    # This method tells SQLAlchemy to save the user to the database.
    # The session.add from SQLAlchemy will create a new user or update it
    # automatically.
    def save_user(self):
        db.session.add(self)
        db.session.commit()

