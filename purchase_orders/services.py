"""Camada de serviço para pedidos de compra.

Centraliza a lógica de negócio, mantendo os resources (endpoints) livres
de regras e validações diretas. Essa separação facilita testes e manutenção.
"""

from flask import jsonify
from .model import PurchaseOrderModel
from exceptions.exceptions import QuantityException

class PurchaseOrdersServices:
    """Fornece métodos de negócio para manipular pedidos de compra."""

    def _check_quantity(self, quantity):
        """
        Valida a quantidade informada.

        A regra de negócio exige que os pedidos tenham entre 50 e 150 itens
        para evitar pedidos inviáveis ou não lucrativos.
        """
        if quantity < 50 or quantity > 150:
            raise QuantityException('A quantidade deve ser entre 50 e 150 itens')

    def find_all(self):
        """Retorna todos os pedidos como lista de dicionários."""
        purchase_orders = PurchaseOrderModel.find_all()
        return [p.as_dict() for p in purchase_orders]
    
    def create(self, **kwargs):
        """
        Cria e salva um novo pedido de compra.

        Antes de salvar, aplica validação de quantidade para garantir
        conformidade com a regra de negócio.
        """
        self._check_quantity(kwargs['quantity'])
        purchase_order = PurchaseOrderModel(**kwargs)
        purchase_order.save()

        return purchase_order.as_dict()
    
    def find_by_id(self, id):
        """Busca um pedido pelo ID e retorna como dicionário, se encontrado."""
        purchase_order = PurchaseOrderModel.find_by_id(id)
        if purchase_order:
            return purchase_order.as_dict()

        return jsonify({'message': 'Pedido de id:{} não encontrado'.format(id)})