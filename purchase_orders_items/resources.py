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
        """Lista os itens de um pedido.
        ---
        security: [{BearerAuth: []}]
        parameters:
          - in: path
            name: id
            type: integer
            required: true
            description: ID do pedido.
        responses:
          200:
            description: Itens do pedido.
            schema:
              type: array
              items:
                type: object
                properties:
                  id: {type: integer}
                  description: {type: string}
                  price: {type: number}
                  quantity: {type: integer}
                  purchase_order_id: {type: integer}
          401:
            description: Token ausente ou inválido.
          404:
            description: Pedido não encontrado.
        """
        return self.__service__.find_by_purchase_order_id(id)

    @jwt_required()
    def post(self, id):
        """Adiciona um item sem ultrapassar a quantidade do pedido.
        ---
        security: [{BearerAuth: []}]
        consumes: [application/json]
        parameters:
          - in: path
            name: id
            type: integer
            required: true
            description: ID do pedido.
          - in: body
            name: item
            required: true
            schema:
              type: object
              required: [description, price, quantity]
              properties:
                description: {type: string}
                price: {type: number, minimum: 0}
                quantity: {type: integer, minimum: 1}
        responses:
          200:
            description: Item criado.
            schema:
              type: object
              properties:
                id: {type: integer}
                description: {type: string}
                price: {type: number}
                quantity: {type: integer}
                purchase_order_id: {type: integer}
          400:
            description: Dados inválidos ou quantidade acima do saldo do pedido.
          401:
            description: Token ausente ou inválido.
          404:
            description: Pedido não encontrado.
        """
        data = PurchaseOrdersItems.parser.parse_args()
        return self.__service__.create(
            data['description'],
            data['price'],
            id,
            data['quantity'],
        )
