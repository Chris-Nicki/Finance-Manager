from app.schemas import ma
from marshmallow import fields

# Define the Customer Schema
class PostSchema(ma.Schema):
    id = fields.Integer(required=False)
    user_id = fields.Integer(required=True)
    title = fields.String(required=True)
    body = fields.String(required=True)
    

post_schema = PostSchema()
posts_schema = PostSchema(many=True)