"""Modelo ORM para itens de pedidos de compra.

Mapeia a tabela 'purchase_orders_items' no banco de dados e provê métodos
para persistência e consulta de itens vinculados a um pedido de compra.
"""

from db import db


class PurchaseOrdersItemsModel(db.Model):
    """Representa um item pertencente a um pedido de compra."""

    __tablename__ = 'purchase_orders_items'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    purchase_order_id = db.Column(db.Integer, db.ForeignKey('purchase_orders.id'), nullable=False)

    def __init__(self, description, price, purchase_order_id, quantity):
        """Cria um item de pedido de compra em memória (não persistido)."""
        self.description = description
        self.price = price
        self.purchase_order_id = purchase_order_id
        self.quantity = quantity

    def as_dict(self):
        """Converte o item em um dicionário para serialização."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def find_by_purchase_order_id(cls, _purchase_order_id):
        """Retorna todos os itens associados a um pedido de compra."""
        return cls.query.filter_by(purchase_order_id=_purchase_order_id).all()

    def save(self):
        """
        Persiste o item no banco de dados.

        Executa commit imediato para refletir o estado mais recente
        em consultas subsequentes.
        """
        db.session.add(self)
        db.session.commit()
