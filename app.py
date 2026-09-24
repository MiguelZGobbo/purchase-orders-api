import os

from flasgger import Swagger
from flask import Flask, current_app, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_jwt_extended.exceptions import JWTExtendedException
from flask_migrate import Migrate
from flask_restful import Api
from jwt.exceptions import PyJWTError
from werkzeug.exceptions import HTTPException

from db import db
from purchase_orders.resources import PurchaseOrders, PurchaseOrdersById
from purchase_orders_items.resources import PurchaseOrdersItems
from users.resources import UserCreation, UserLogin


class JWTResourceApi(Api):
    def handle_error(self, error):
        if isinstance(error, JWTExtendedException | PyJWTError):
            return current_app.handle_user_exception(error)
        return super().handle_error(error)


def create_app():
    jwt_secret_key = os.getenv('JWT_SECRET_KEY')
    if not jwt_secret_key:
        raise RuntimeError('Configure JWT_SECRET_KEY antes de iniciar a aplicação')

    app = Flask(__name__)
    api = JWTResourceApi(app)
    CORS(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI', 'sqlite:///default.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = jwt_secret_key
    app.config['SWAGGER'] = {
        'title': 'Purchase Orders API',
        'description': 'API REST para gerenciamento de pedidos de compra com autenticação JWT',
        'version': '1.0.0',
    }

    db.init_app(app)
    jwt = JWTManager(app)
    Swagger(
        app,
        template={
            'securityDefinitions': {
                'BearerAuth': {
                    'type': 'apiKey',
                    'name': 'Authorization',
                    'in': 'header',
                    'description': 'Informe Bearer <token> obtido em POST /login.',
                }
            }
        },
    )

    @jwt.invalid_token_loader
    def invalid_jwt(error):
        return ({'message': 'Token de acesso inválido'}, 401)

    @jwt.unauthorized_loader
    def unauthorized_jwt(error):
        return ({'message': 'Sem autorização, por favor informe um token válido'}, 401)

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
        """Informações da API.
        ---
        responses:
          200:
            description: Nome, versão e caminho da documentação.
            schema:
              type: object
              properties:
                name: {type: string}
                version: {type: string}
                docs: {type: string}
        """
        return jsonify(
            {
                'name': 'Purchase Orders API',
                'version': '1.0.0',
                'docs': '/apidocs',
            }
        )

    @app.route('/health')
    def health():
        """Verifica a disponibilidade da aplicação.
        ---
        responses:
          200:
            description: Aplicação ativa.
            schema:
              type: object
              properties:
                status: {type: string, enum: [healthy]}
        """
        return jsonify({'status': 'healthy'}), 200

    return app
