from flask import jsonify
from flask_restful import Resource, reqparse

purchase_orders = [
    {
        'id': 1,
        'description': 'Pedido 1',
        'items': [
            {
                'id': 1,
                'description': 'Laranja',
                'price': 5.75
            }
        ]
    }
]

class PurchaseOrders(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'id',
        type = int,
        required = True,
        help = 'Informe o ID do pedido'
    )

    parser.add_argument(
        'description',
        type = str,
        required = True,
        help = 'Informe a descrição do produto'
    )

    def get(self):
        return jsonify(purchase_orders)
    
    def post(self):
        data = PurchaseOrders.parser.parse_args()

        purchase_order = {
            'id': data['id'],
            'description': data['description'],
            'items': []
        }

        purchase_orders.append(purchase_order)
        return jsonify(purchase_order)