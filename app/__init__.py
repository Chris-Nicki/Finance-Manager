import os
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from app.database import db, migrate 
from app.limiter import limiter
from app.caching import cache
from app.swagger_docs import swaggerui_blueprint
from dotenv import load_dotenv
from flask_limiter.util import get_remote_address

# Create an instance of the flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 


#Initialize the app with the flask-sqlalchemy
db.init_app(app)

# Initialize the app and db with migrate
migrate.init_app(app, db)

# Initialize the app with flask-limiter
limiter.init_app(app)

# Initialize the app with flask-caching
cache.init_app(app)

# Register the Swagger UI Blueprint
app.register_blueprint(swaggerui_blueprint)

from app.routes import *



if __name__ == '__main__':
    app.run(debug=True)