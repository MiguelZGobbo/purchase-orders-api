"""Modelo ORM para pedidos de compra.

Mapeia a tabela 'purchase_orders' no banco de dados, fornecendo métodos
de persistência e consulta. O uso do SQLAlchemy abstrai SQL manual,
reduzindo erros e aumentando a manutenibilidade.
"""
from db import db

class PurchaseOrderModel(db.Model):
    """Representa um pedido de compra armazenado na tabela 'purchase_orders'."""
    __tablename__ = 'purchase_orders'

    id  = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String, nullable = False)
    quantity = db.Column(db.Integer, nullable = False)

    def __init__(self, description, quantity):
        """Cria um objeto de pedido de compra em memória (não persistido)."""
        self.description = description
        self.quantity = quantity

    def as_dict(self):
        """
        Converte o modelo em um dicionário.

        Útil para serializar o objeto em respostas JSON da API.
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def find_all(cls):
        """Retorna todos os pedidos cadastrados no banco."""
        return cls.query.all() # Executa o select * from purchase_order do DB
    
    @classmethod
    def find_by_id(cls, _id):
        """Retorna um pedido pelo ID ou None se não encontrado."""
        return cls.query.filter_by(id = _id).first()
    
    def save(self):
        """
        Persiste o pedido no banco de dados.

        Executa um commit imediato para que a instância esteja disponível
        para consultas subsequentes.
        """
        db.session.add(self)
        db.session.commit()
    
