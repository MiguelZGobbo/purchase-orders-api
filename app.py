from flask import Flask
from flask_restful import Api
from purchase_orders.resources import PurchaseOrders, PurchaseOrdersById

def create_app():

    app = Flask(__name__)
    api = Api(app)

    api.add_resource(PurchaseOrders, '/purchase_orders')
    api.add_resource(PurchaseOrdersById, '/purchase_orders/<int:id>')

    return app


