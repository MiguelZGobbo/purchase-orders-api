from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from .services import PurchaseOrdersItemsServices


class PurchaseOrdersItems(Resource):
    __service__ = PurchaseOrdersItemsServices()

    parser = reqparse.RequestParser()
    parser.add_argument(
        'description',
        type=str,
        required=True,
        help='Informe uma descrição válida!',
    )
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help='Informe um preço válido!',
    )
    parser.add_argument(
        'quantity',
        type=int,
        required=True,
        help='Informe uma quantidade válida!',
    )

    @jwt_required()
    def get(self, id):
        return self.__service__.find_by_purchase_order_id(id)

    @jwt_required()
    def post(self, id):
        data = PurchaseOrdersItems.parser.parse_args()
        return self.__service__.create(
            data['description'],
            data['price'],
            id,
            data['quantity'],
        )
