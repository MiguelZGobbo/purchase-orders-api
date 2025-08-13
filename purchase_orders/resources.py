"""Endpoints REST para pedidos de compra.

Define as rotas da API relacionadas a pedidos de compra, aplicando autenticação
via JWT e delegando a lógica de negócio para a camada de serviços.
"""

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from .services import PurchaseOrdersServices

class PurchaseOrders(Resource):
    """Resource para operações em lote de pedidos de compra."""

    __service__ = PurchaseOrdersServices()

    # Define e valida parâmetros de entrada para POST
    parser = reqparse.RequestParser()
    parser.add_argument(
        'description',
        type = str,
        required = True,
        help = 'Informe uma descrição válida'
    )

    parser.add_argument(
        'quantity',
        type = int,
        required = True,
        help = 'Informe uma quantidade válida'
    )

    @jwt_required()
    def get(self):
        """Retorna todos os pedidos cadastrados (requer autenticação)."""
        return self.__service__.find_all()

    @jwt_required()
    def post(self):
        """
        Cria um novo pedido (requer autenticação).

        Os dados são validados pelo parser antes de chegar à camada de serviço.
        """
        data = PurchaseOrders.parser.parse_args()

        return self.__service__.create(**data)
    
class PurchaseOrdersById(Resource):
    """Resource para operações em um pedido específico pelo ID."""

    __sevice__ = PurchaseOrdersServices()

    @jwt_required()
    def get(self, id):
        """Retorna um pedido pelo ID (requer autenticação)."""
        return self.__sevice__.find_by_id(id)
            
    