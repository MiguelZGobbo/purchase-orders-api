import pytest

from exceptions.exceptions import QuantityException
from purchase_orders_items.model import PurchaseOrdersItemsModel
from purchase_orders_items.services import PurchaseOrdersItemsServices


def test_check_maximum_po_quantity(seed_db, test_client):
    with test_client.application.app_context():
        with pytest.raises(QuantityException) as ex:
            PurchaseOrdersItemsServices()._check_maximum_purchase_order_quantity(
                seed_db['purchase_order'].id,
                seed_db['purchase_order'].quantity,
                30,
            )
        assert ex.value.code == 400
        assert ex.value.description == 'Você só pode adicionar mais 20 itens'


def test_create_accepts_exact_remaining_quantity(seed_db, test_client):
    with test_client.application.app_context():
        order_id = seed_db['purchase_order'].id
        result = PurchaseOrdersItemsServices.create('Último item', 10, order_id, 20)
        assert result['quantity'] == 20
        assert (
            sum(
                item.quantity
                for item in PurchaseOrdersItemsModel.find_by_purchase_order_id(order_id)
            )
            == 50
        )


def test_create_rejects_excess_without_persisting(seed_db, test_client):
    with test_client.application.app_context():
        order_id = seed_db['purchase_order'].id
        with pytest.raises(QuantityException, match='Você só pode adicionar mais 20 itens'):
            PurchaseOrdersItemsServices.create('Excedente', 10, order_id, 21)
        assert (
            sum(
                item.quantity
                for item in PurchaseOrdersItemsModel.find_by_purchase_order_id(order_id)
            )
            == 30
        )
