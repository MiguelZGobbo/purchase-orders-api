from db import db

class PurchaseOrderModel(db.Model):
    __tablename__ = 'purchase_orders'

    id  = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String, nullable = False)

    def __init__(self, description):
        self.description = description

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def find_all(cls):
        return cls.query.all() # Executa o select * from purchase_order do DB
    
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id = _id).first()
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
