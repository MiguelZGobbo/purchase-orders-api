from typing import Any

from exceptions.exceptions import QuantityException
from purchase_orders.model import PurchaseOrderModel

from .model import PurchaseOrdersItemsModel


class PurchaseOrdersItemsServices:
    @staticmethod
    def _check_maximum_purchase_order_quantity(
        purchase_order_id: int,
        purchase_order_quantity: int,
        quantity: int,
    ) -> None:
        purchase_orders_items = PurchaseOrdersItemsModel.find_by_purchase_order_id(
            purchase_order_id,
        )

        sum_items = sum(poi.quantity for poi in purchase_orders_items)

        if sum_items + quantity > purchase_order_quantity:
            remaining = purchase_order_quantity - sum_items
            raise QuantityException(f'Você só pode adicionar mais {remaining} itens')

    @staticmethod
    def find_by_purchase_order_id(
        purchase_order_id: int,
    ) -> list[dict[str, Any]] | tuple[dict[str, str], int]:
        purchase_order = PurchaseOrderModel.find_by_id(purchase_order_id)
        if purchase_order:
            items = PurchaseOrdersItemsModel.find_by_purchase_order_id(purchase_order_id)
            return [p.as_dict() for p in items]
        return {'message': f'Pedido de id:{purchase_order_id} não encontrado!'}, 404

    @staticmethod
    def create(
        description: str,
        price: float,
        purchase_order_id: int,
        quantity: int,
    ) -> dict[str, Any] | tuple[dict[str, str], int]:
        purchase_order = PurchaseOrderModel.find_by_id(purchase_order_id)
        if purchase_order:
            PurchaseOrdersItemsServices._check_maximum_purchase_order_quantity(
                purchase_order_id,
                purchase_order.quantity,
                quantity,
            )
            item = PurchaseOrdersItemsModel(description, price, purchase_order_id, quantity)
            item.save()
            return item.as_dict()
        return {'message': f'Pedido de id:{purchase_order_id} não encontrado'}, 404
