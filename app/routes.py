from . import app, db, limiter, cache
from flask import request, redirect, url_for
from app.schemas.userSchema import user_input_schema, user_output_schema, users_schema, user_login_schema
from app.schemas.postSchema import post_schema, posts_schema
from app.schemas.commentsSchema import comment_schema, comments_schema
from marshmallow import ValidationError
from app.models import User, Post, Comment, Role
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils.util import encode_token
# from app.auth import token_auth


@app.route('/')
def index():
    return 'Hello'

#################
  #User Routes#
#################

# Create a new customer
@app.route('/users', methods=["POST"])
def create_user():
    if not request.is_json:
        return {"error": "Request body must be application/json"}, 400 # Bad Request by Client
    try:
        data = request.json
        user_data = user_input_schema.load(data)
        # Query the customer table to see if any customer have that username or email
        query = db.select(User).where((User.username == user_data['username']) | (User.email == user_data['email']))
        check_users = db.session.scalars(query).all()
        if check_users: # If there are customers in the check_customers list (empty list evaluates to False)
            return {"error": "Customer with that username and/or email already exists"}, 400 # Bad Request by client
        new_user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            username=user_data['username'],
            password=generate_password_hash(user_data['password'])
        )
        # and add to the database
        db.session.add(new_user)
        db.session.commit()
        # Serialize the new customer object and return with 201 status
        return user_output_schema.jsonify(new_user), 201 # Created - Success
    except ValidationError as err:
        return err.messages, 400
    except ValueError as err:
        return {"error": str(err)}, 400

# Get ALL USERS
@app.route('/users', methods=['GET'])
@cache.cached(timeout=60)
def get_all_users():
    # Get the query parameters from the request
    args = request.args
    page = args.get('page', 1, type=int)
    per_page = args.get('per_page', 10, type=int)
    search = args.get('search', '')
    query = db.select(User).where(User.username.like(f'%{search}%')).limit(per_page).offset((page-1)*per_page)
    users = db.session.scalars(query).all()
    return users_schema.jsonify(users)

# Get a single user by ID
@app.route('/users/<int:user_id>', methods=["GET"])
def get_single_user(user_id):
    customer = db.session.get(User, user_id)
    if customer is not None:
        return user_output_schema.jsonify(customer)
    return {"error": f"User with ID {user_id} does not exist"}, 404 # Not Found