from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import post_load, fields, ValidationError
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


# Models
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    price = db.Column(db.Float, nullable=False)
    inventory_quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self) -> str:
        return f"{self.name} Description: {self.description} Price: ${self.price} Inventory: {self.inventory_quantity}"

# Schemas
class ProductSchema(ma.Schema):
    id = fields.Integer(primary_key=True)
    name = fields.String(required=True)
    description = fields.String()
    price = fields.Float(required=True)
    inventory_quantity = fields.Integer(required=True)

    class Meta:
        fields = ("id", "name", "description", "price", "inventory_quantity")

    @post_load
    def create_product(self, data, **kwargs):
        return Product(**data)

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# Resources
class ProductListResource(Resource):
    def get(self):
        all_products = Product.query.all()
        return products_schema.dump(all_products) 
    
    def post(self):
        form_data = request.get_json()
        try:
            new_product = product_schema.load(form_data)
            db.session.add(new_product)
            db.session.commit()
            return product_schema.dump(new_product), 201
        except ValidationError as err:
            return err.messages, 400
    
class ProductResource(Resource):
    def get(self, pk):
        product_from_db = Product.query.get_or_404(pk)
        return product_schema.dump(product_from_db)

    def delete(self, pk):
        product_from_db = Product.query.get_or_404(pk)
        db.session.delete(product_from_db)
        db.session.commit()
        return '', 204
    
    def put(self, pk):
        product_from_db = Product.query.get_or_404(pk)
        
        if 'name' in request.json:
            product_from_db.name = request.json['name']
        if 'description' in request.json:
            product_from_db.description = request.json['description']
        if 'price' in request.json:
            product_from_db.price = request.json['price']
        if 'inventory_quantity' in request.json:
            product_from_db.inventory_quantity = request.json['inventory_quantity']

        db.session.commit()
        return product_schema.dump(product_from_db)
        
# Routes
api.add_resource(ProductListResource, '/api/products/')
api.add_resource(ProductResource, '/api/products/<int:pk>')

