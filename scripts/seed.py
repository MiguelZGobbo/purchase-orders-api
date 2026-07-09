import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import create_app
from db import db
from purchase_orders.model import PurchaseOrderModel
from purchase_orders_items.model import PurchaseOrdersItemsModel
from users.model import UserModel


def seed():
    app = create_app()

    with app.app_context():
        db.create_all()

        if UserModel.find_user_by_email('admin@example.com'):
            print('Banco já possui dados. Pulando seed.')
            return

        user = UserModel('admin@example.com', '123456')
        db.session.add(user)

        po1 = PurchaseOrderModel('Pedido de materiais de escritório', 100)
        db.session.add(po1)

        po2 = PurchaseOrderModel('Pedido de equipamentos de TI', 80)
        db.session.add(po2)

        db.session.flush()

        items = [
            PurchaseOrdersItemsModel('Canetas azuis', 2.50, po1.id, 50),
            PurchaseOrdersItemsModel('Papel A4 (resma)', 22.90, po1.id, 30),
            PurchaseOrdersItemsModel('Pastas arquivo', 5.75, po1.id, 20),
            PurchaseOrdersItemsModel('Teclado mecânico', 199.90, po2.id, 30),
            PurchaseOrdersItemsModel('Mouse sem fio', 89.90, po2.id, 30),
            PurchaseOrdersItemsModel('Monitor 24"', 899.00, po2.id, 20),
        ]
        db.session.add_all(items)
        db.session.commit()

        print('Banco populado com sucesso!')
        print('  Usuário: admin@example.com / 123456')
        print(f'  Pedidos: {po1.id}, {po2.id}')
        print(f'  Itens: {len(items)}')


if __name__ == '__main__':
    seed()
