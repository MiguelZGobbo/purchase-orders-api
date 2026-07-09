import pytest

from exceptions.exceptions import QuantityException
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
