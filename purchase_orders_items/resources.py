from flask_restful import Resource, reqparse
from flask import jsonify

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

class PurchaseOrdersItems(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument(
        'id',
        type = int,
        required = True,
        help = "Informe um ID"
    )

    parser.add_argument(
        'description',
        type =  str,
        required = True,
        help = "Informe uma descrição"
    )

    parser.add_argument(
        'price',
        type = float,
        required = True,
        help = "Informe o preço"
    )

    def get(self, id):
        for po in purchase_orders:
            if po['id'] == id:
                return jsonify(po["items"])
        return ("Id não encontrado!")
    
    def post(self, id):
        request_data = PurchaseOrdersItems().parser.parse_args()

        for po in purchase_orders:
            if po['id'] == id:
                po['items'].append({
                    'id': request_data['id'],
                    'description': request_data['description'],
                    'price': request_data['price']
                })

                return jsonify(po)       
                
        return ("Id não encontrado")

    