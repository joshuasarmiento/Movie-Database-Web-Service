from flask import Flask, render_template, jsonify
from flask_restful import request, abort, Api, Resource, reqparse 

app = Flask(__name__)
api = Api(app)

#root (“/”) route
@app.route('/')
def index():
    return render_template('index.html')

#rendering an index.html template and on  “/manage”
@app.route('/manage')
def crud():
    return render_template('manage.html')

PRODUCTS = {
    1 : {"id" : 1, 
        "name" : "Pastry", 
        "price" : 10, 
        "qty" : 5,
        "exp" : "July 22, 2021",
        },
    2 : {"id" : 2, 
        "name" : "Cookies", 
        "price" : 5, 
        "qty" : 4,
        "exp" : "July 22, 2021",
        },
    3 : {"id" : 3, 
        "name" : "Doughnut", 
        "price" : 15, 
        "qty" : 10,
        "exp" : "July 30, 2021",
        },       
}

class ProductList(Resource):
    # GET request at “/api”
    # 
    def get(self):
        response_data = { "data" : [ product_data for id, product_data in PRODUCTS.items()] }
        return response_data

    # POST request at “/api” 
    def post(self):
        request_data = request.get_json(force=True)

        # If the entry does not exist
        if not request_data \
           or not 'name' in request_data \
           or not 'price' in request_data \
           or not 'qty' in request_data \
           or not 'exp' in request_data:
           abort(400)

        # Create new Product
        new_product_id = int(max(PRODUCTS.keys())) + 1
        new_product = {
            "id" : new_product_id,
            "name" : request_data["name"],
            "price" : request_data["price"],
            "qty" : request_data["qty"],
            "exp" : request_data["exp"]
        }

        PRODUCTS[new_product_id] = new_product

class ProductbyID(Resource):
    
    # GET request at “/api/<id>”
    def get(self, id):
        # If the entry does not exist
        if id not in PRODUCTS:
            return abort(404, message="No such record exists!")
        # Get by ID
        return [product_data for id, product_data in PRODUCTS.items()][id - 1]

    #  PUT request at “/api/<id>”
    def put(self, id):

        # https://flask-restful.readthedocs.io/en/latest/reqparse.html
        # I used reqparse to simply access to any variable on the flask.request
        
        #request_data = request.get_json(force=True)
        request.get_json(force=True)
        parcer = reqparse.RequestParser()

        """
        # in request_data 
        if 'name' in type(request_data['name']) is not str:
            return abort(400)
        if 'price' in type(request_data['price']) is not int:
            return abort(400)
        if 'qty' in type(request_data['qty']) is not int:
            return abort(400)
        if 'exp' in type(request_data['exp']) is not str:
           return abort(400)
        """
        # two arguments in the Request values <an integer and a string>
        # The default argument type is a unicode string.
        parcer.add_argument("name", type=str)
        parcer.add_argument("price", type=int)
        parcer.add_argument("qty", type=int)
        # The default argument type is a unicode string.
        parcer.add_argument("exp", type=str)
        p = parcer.parse_args()
       
        if p["name"]:
            PRODUCTS[id]["name"] = p["name"]
        if p["price"]:
            PRODUCTS[id]["price"] = p["price"]
        if p["qty"]:
            PRODUCTS[id]["qty"] = p["qty"]
        if p["exp"]:
            PRODUCTS[id]["exp"] = p["exp"]

        # If the request data is invalid 
        if id not in PRODUCTS:
            return abort(400)

        return PRODUCTS[id]

    # POST request at “/api/<id>”
    def delete(self, id):
        # If the entry does not exist    
        if id not in PRODUCTS:
            return abort(404, message="No such record exists!")
        
        prod = PRODUCTS
        # prod.remove(id)
        del prod[id]
        return PRODUCTS

# Set up the API resource routing:

api.add_resource(ProductList, '/api')
# resource routing with ID
api.add_resource(ProductbyID, '/api/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)       
