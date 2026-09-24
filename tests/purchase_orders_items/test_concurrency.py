"""Integração concorrente: requer TEST_POSTGRES_URI para um banco de teste PostgreSQL."""

import os
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier, BrokenBarrierError

import pytest
from flask_jwt_extended import create_access_token
from sqlalchemy import event

from app import create_app
from db import db
from purchase_orders.model import PurchaseOrderModel
from purchase_orders_items.model import PurchaseOrdersItemsModel


@pytest.mark.nocleardb
def test_concurrent_item_creation_respects_order_limit(monkeypatch):
    postgres_uri = os.getenv('TEST_POSTGRES_URI')
    if not postgres_uri:
        pytest.skip('Defina TEST_POSTGRES_URI para executar a concorrência no PostgreSQL')

    monkeypatch.setenv('DB_URI', postgres_uri)
    app = create_app()
    barrier = Barrier(2)
    read_barrier = Barrier(2)

    with app.app_context():
        db.create_all()
        order = PurchaseOrderModel('Teste concorrente', 50)
        db.session.add(order)
        db.session.commit()
        order_id = order.id
        token = create_access_token(identity='concurrency-test')
        engine = db.engine
        db.session.remove()

    def synchronize_item_reads(connection, cursor, statement, parameters, context, executemany):
        if 'FROM purchase_orders_items' in statement:
            try:
                read_barrier.wait(timeout=2)
            except BrokenBarrierError:
                pass

    event.listen(engine, 'before_cursor_execute', synchronize_item_reads)

    def add_item():
        with app.test_client() as client:
            barrier.wait(timeout=10)
            response = client.post(
                f'/purchase_orders/{order_id}/items',
                json={'description': 'Item concorrente', 'price': 1, 'quantity': 30},
                headers={'Authorization': f'Bearer {token}'},
            )
            return response.status_code, response.json

    try:
        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = [executor.submit(add_item) for _ in range(2)]
            results = [future.result(timeout=20) for future in futures]

        assert sorted(status for status, _ in results) == [200, 400]
        assert next(body for status, body in results if status == 400) == {
            'message': 'Você só pode adicionar mais 20 itens'
        }
        with app.app_context():
            items = PurchaseOrdersItemsModel.find_by_purchase_order_id(order_id)
            assert sum(item.quantity for item in items) == 30
    finally:
        event.remove(engine, 'before_cursor_execute', synchronize_item_reads)
        with app.app_context():
            db.session.query(PurchaseOrdersItemsModel).filter_by(
                purchase_order_id=order_id
            ).delete()
            db.session.query(PurchaseOrderModel).filter_by(id=order_id).delete()
            db.session.commit()
            db.session.remove()
