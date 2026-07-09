"""Configurações e fixtures para os testes de purchase_orders."""

import pytest

from db import db
from purchase_orders.model import PurchaseOrderModel
from purchase_orders_items.model import PurchaseOrdersItemsModel


@pytest.fixture()
def seed_db():
    """
    Insere um pedido de compra no banco para uso nos testes.

    Essa fixture cria um registro consistente que pode ser reutilizado
    em diferentes testes, evitando duplicação de código.
    """
    po = PurchaseOrderModel('Purchase Order Teste', 50)
    db.session.add(po)
    db.session.commit()

    yield po


@pytest.fixture(scope='function', autouse='True')
def clear_db(request):
    """
    Limpa as tabelas de itens e pedidos antes de cada teste.

    Executa automaticamente, a menos que o teste tenha o marcador 'nocleardb',
    garantindo isolamento e prevenindo que dados de um teste interfiram em outro.
    """
    if 'nocleardb' in request.keywords:
        return
    db.session.query(PurchaseOrdersItemsModel).delete()
    db.session.query(PurchaseOrderModel).delete()
    db.session.commit()
