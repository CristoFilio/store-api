from flask_restful import Resource, reqparse
from models.user import UserModel


# RegisterUser is used as a Resource from flask_restful.
# Flask restful resources are able to receive CRUD requests using
# methods within them.
class RegisterUser(Resource):
    # reqparse is used to validate the data provided by the request.
    # In this case it will format the data to only contain the arguments
    # we want, which are username and password. Anything else gets discarded
    # from the data.
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='This field is required')
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='This field is required')
    created = {'message': 'User created successfully. Welcome!'}
    exists = {'message': 'That username is already in use. Please enter a new one'}

    # The post method first gives the username data from the parser to the
    # class method find user inside UserModel. This will return an object
    # if the user exists, and None if the user is not found.
    # If the user is found then return the exists message and the 400 code, else
    # create a user which is a UserModel instance by giving it the packed data,
    # which contains the username and password, and provide the access level.
    # Call the save user method in the user object to save the user to the database
    # (this is all done using SQLALchemy), then return created message and 201.
    def post(self):
        data = RegisterUser.parser.parse_args()

        if UserModel.find_user(data['username']):
            return RegisterUser.exists, 400
        # Create user in database.
        user = UserModel(**data, access=1)
        user.save_user()
        return RegisterUser.created, 201
