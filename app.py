from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Api, Resource
from dotenv import load_dotenv
from os import environ

load_dotenv()

# Create App instance
app = Flask(__name__)

# Add DB URI from .env
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('SQLALCHEMY_DATABASE_URI')

# Registering App w/ Services
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)
CORS(app)
Migrate(app, db)


'''(5 points): As a developer, I want to build a REST web API in Flask, 
so that I can make HTTP requests interact with the data set.'''

# Models
'''
Create your database model(s) in app.py with the required properties, then run:
flask db init (Creates tables)
flask db migrate -m "Init" (Creates migration)
flask db upgrade (Runs migration)
'''

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    price = db.Column(db.Float, nullable=False)
    inventory_quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self) -> str:
        return f"{self.name} Description: {self.description} Price: ${self.price} Inventory: {self.inventory_quantity}"

# Schemas

'''Create Marshmallow Schema in app.py'''

# Resources

'''(5 points): As a developer, I want to create a GET endpoint that responds 
with a 200 success status code and all of the products within the Product table.
(5 points): As a developer, I want to create a GET by id endpoint that does 
the following things: 
Accepts a value from the requests URL (The id of the product to retrieve).
Returns a 200 status code. (Explicitly return this, not just allow it to default)
Responds with the product in the database that has the id that was sent through the URL. 

(5 points): As a developer, I want to create a POST endpoint that does the following things: 
Accepts a body object from the request in the form of a Product model. 
Adds the new product to the database. 
Returns a 201 status code. 
Responds with the newly created product object.

(5 points): As a developer, I want to create a PUT endpoint that does the following things: 
Accepts a value from the requests URL (The id of the product to be updated). 
Accepts a body object from the request in the form of a Product model. 
Finds the product in the Product table and updates that product with the properties 
that were sent in the requests body. 
Returns a 200 status code.  (Explicitly return this, not just allow it to default)
Responds with the newly updated product object. 

(5 points): As a developer,  I want to create a DELETE endpoint that does the following things: 
Accepts a value from the requests URL. 
Deletes the Product from the database.
Returns a 204 status code (NO CONTENT).
'''


# Routes

'''(5 points): As a developer, I want to build a REST web API in Flask, 
so that I can make HTTP requests interact with the data set.'''

'''(5 points): As a developer, I want my API to serve content on the following url paths:
Paths must match these exactly!
127.0.0.1:5000/api/products/ 
127.0.0.1:5000/api/products/<int:pk>
'''

# 127.0.0.1:5000/api/products/
# 127.0.0.1:5000/api/products/<int:pk>

'''(5 points): As a developer, I want to use Postman to make a 
POST, PUT, DELETE, and both GET requests (get by id and get all) 
request to my REST web API, save it to a collection, 
and then export it as a JSON from Postman.'''

'''Be sure to include the exported JSON file in your project folder and push it to GitHub!'''