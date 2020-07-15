from models.user import UserModel


# Authenticate and identity are used by jwt to find and generate log in tokens.

# Authenticate gives the username to the UserModel class function to create
# a UserModel object with the user information, or return None if not found.
def authenticate(username, password):
    user = UserModel.find_user(username)
    # if a UserModel object was created from that username, compare the password
    # of the object to the password provided. If the password is the same, return
    # the object to jwt to generate a log in token.
    if user and user.password == password:
        return user


# JWT gives the identity function an object with the encrypted token and id.
# identity gives the identity key to the UserModel object to find the user in
# the database with an id, and returns an object with the information to jwt
# to validate the token.
def identity(payload):
    _id = payload['identity']
    return UserModel.find_user(_id=_id)


