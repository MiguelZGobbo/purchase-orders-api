"""Configurações e fixtures para os testes de purchase_orders_items."""

import pytest

from db import db
from purchase_orders.model import PurchaseOrderModel
from purchase_orders_items.model import PurchaseOrdersItemsModel


@pytest.fixture()
def seed_db():
    """
    Insere um pedido de compra e um item associado no banco para uso nos testes.

    Essa fixture cria registros consistentes que podem ser reutilizados em diferentes
    testes, garantindo a existência de um pedido de compra com um item associado
    para validação dos cenários de teste.
    """
    po = PurchaseOrderModel('Pedido de Testes', 50)
    db.session.add(po)
    db.session.commit()

    poi = PurchaseOrdersItemsModel('Item 1', 8.99, po.id, 30)
    db.session.add(poi)
    db.session.commit()

    yield {'purchase_order': po, 'items': poi}


@pytest.fixture(scope='function', autouse=True)
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
