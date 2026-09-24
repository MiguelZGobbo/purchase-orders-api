from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from .services import PurchaseOrdersServices


class PurchaseOrders(Resource):
    __service__ = PurchaseOrdersServices()

    parser = reqparse.RequestParser()
    parser.add_argument(
        'description',
        type=str,
        required=True,
        help='Informe uma descrição válida',
    )
    parser.add_argument(
        'quantity',
        type=int,
        required=True,
        help='Informe uma quantidade válida',
    )

    @jwt_required()
    def get(self):
        """Lista todos os pedidos.
        ---
        security: [{BearerAuth: []}]
        responses:
          200:
            description: Pedidos cadastrados, visíveis a qualquer usuário autenticado.
            schema:
              type: array
              items:
                type: object
                properties:
                  id: {type: integer}
                  description: {type: string}
                  quantity: {type: integer}
          401:
            description: Token ausente ou inválido.
        """
        return self.__service__.find_all()

    @jwt_required()
    def post(self):
        """Cria um pedido de compra.
        ---
        security: [{BearerAuth: []}]
        consumes: [application/json]
        parameters:
          - in: body
            name: order
            required: true
            schema:
              type: object
              required: [description, quantity]
              properties:
                description: {type: string}
                quantity: {type: integer, minimum: 50, maximum: 150}
        responses:
          200:
            description: Pedido criado.
            schema:
              type: object
              properties:
                id: {type: integer}
                description: {type: string}
                quantity: {type: integer}
          400:
            description: Dados inválidos ou quantidade fora de 50 a 150.
          401:
            description: Token ausente ou inválido.
        """
        data = PurchaseOrders.parser.parse_args()
        return self.__service__.create(data['description'], data['quantity'])


class PurchaseOrdersById(Resource):
    __service__ = PurchaseOrdersServices()

    @jwt_required()
    def get(self, id):
        """Consulta um pedido pelo ID.
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
            description: Pedido encontrado.
            schema:
              type: object
              properties:
                id: {type: integer}
                description: {type: string}
                quantity: {type: integer}
          401:
            description: Token ausente ou inválido.
          404:
            description: Pedido não encontrado.
        """
        return self.__service__.find_by_id(id)
