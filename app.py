import os

from flasgger import Swagger
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_restful import Api
from werkzeug.exceptions import HTTPException

from db import db
from purchase_orders.resources import PurchaseOrders, PurchaseOrdersById
from purchase_orders_items.resources import PurchaseOrdersItems
from users.resources import UserCreation, UserLogin


def create_app():
    app = Flask(__name__)
    api = Api(app)
    CORS(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI', 'sqlite:///default.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv(
        'JWT_SECRET_KEY',
        'super-secret-key-change-in-production',
    )
    app.config['SWAGGER'] = {
        'title': 'Purchase Orders API',
        'description': 'API REST para gerenciamento de pedidos de compra com autenticação JWT',
        'version': '1.0.0',
    }

    db.init_app(app)
    jwt = JWTManager(app)
    Swagger(app)

    @jwt.invalid_token_loader
    def invalid_jwt(error):
        return ({'message': 'Token de acesso inválido'}, 401)

    @jwt.unauthorized_loader
    def unauthorized_jwt(error):
        return ({'message': 'Sem autorização, por favor informe um token válido'}, 401)

    with app.app_context():
        db.create_all()

    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        return jsonify({'message': error.description}), error.code

    Migrate(app, db)

    api.add_resource(PurchaseOrders, '/purchase_orders')
    api.add_resource(PurchaseOrdersById, '/purchase_orders/<int:id>')
    api.add_resource(PurchaseOrdersItems, '/purchase_orders/<int:id>/items')
    api.add_resource(UserCreation, '/users')
    api.add_resource(UserLogin, '/login')

    @app.route('/')
    def index():
        return jsonify(
            {
                'name': 'Purchase Orders API',
                'version': '1.0.0',
                'docs': '/apidocs',
            }
        )

    @app.route('/health')
    def health():
        return jsonify({'status': 'healthy'}), 200

    return app
