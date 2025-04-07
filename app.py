from flask import Flask
from flask_restful import Api
from purchase_orders.resources import PurchaseOrders, PurchaseOrdersById
from purchase_orders_items.resources import PurchaseOrdersItems
from db import db
from flask_migrate import Migrate

def create_app(env):

    app = Flask(__name__)
    api = Api(app)

    database = 'python_course'

    if env == 'testing':
        database = 'python_course_test'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/{}'.format(database)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)


    with app.app_context():
        db.create_all()

    Migrate(app, db)

    api.add_resource(PurchaseOrders, '/purchase_orders')
    api.add_resource(PurchaseOrdersById, '/purchase_orders/<int:id>')
    api.add_resource(PurchaseOrdersItems, '/purchase_orders/<int:id>/items')

    return app


