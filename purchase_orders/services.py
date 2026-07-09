from typing import Any

from exceptions.exceptions import QuantityException

from .model import PurchaseOrderModel


class PurchaseOrdersServices:
    @staticmethod
    def _check_quantity(quantity: int) -> None:
        if quantity < 50 or quantity > 150:
            raise QuantityException('A quantidade deve ser entre 50 e 150 itens')

    @staticmethod
    def find_all() -> list[dict[str, Any]]:
        purchase_orders = PurchaseOrderModel.find_all()
        return [p.as_dict() for p in purchase_orders]

    @staticmethod
    def create(description: str, quantity: int) -> dict[str, Any]:
        PurchaseOrdersServices._check_quantity(quantity)
        purchase_order = PurchaseOrderModel(description, quantity)
        purchase_order.save()
        return purchase_order.as_dict()

    @staticmethod
    def find_by_id(id: int) -> dict[str, Any] | tuple[dict[str, str], int]:
        purchase_order = PurchaseOrderModel.find_by_id(id)
        if purchase_order:
            return purchase_order.as_dict()
        return {'message': f'Pedido de id:{id} não encontrado'}, 404
