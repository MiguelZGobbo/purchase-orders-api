from flask import Flask, jsonify
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

purchase_orders = [
    {
        'id': 1,
        'description': 'Pedido compra 1',
        'items': [
            {
                'id': 1,
                'description': 'item pedido 1',
                'price': 29.99
            }
        ]
    }
]

class PurchaseOrders(Resource):
    def get(self):
        return jsonify(purchase_orders)
    
api.add_resource(PurchaseOrders, '/purchase_orders')


app.run(port=5000)

