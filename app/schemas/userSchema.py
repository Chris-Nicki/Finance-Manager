from app.schemas import ma
from marshmallow import fields

# Define the Customer Schema
class UserSchema(ma.Schema):
    id = fields.Integer(required = False) # ID is auto generated
    first_name = fields.String(required = True)
    last_name = fields.String(required= True)
    email = fields.String(required= True)
    username = fields.String(required= True)
    password = fields.String(required= True)
    role_id = fields.Int(required=True)

user_input_schema = UserSchema()
user_output_schema = UserSchema(exclude=["password"])
users_schema = UserSchema(many=True, exclude=["password"])
user_login_schema = UserSchema(only=["username", "password"] )