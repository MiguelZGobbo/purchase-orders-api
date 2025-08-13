"""Configuração e inicialização da aplicação Flask."""

import os
from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from db import db

from purchase_orders.resources import PurchaseOrders, PurchaseOrdersById
from purchase_orders_items.resources import PurchaseOrdersItems
from users.resources import UserCreation, UserLogin

def create_app():
    """
    Cria e configura a aplicação Flask.

    Inicializa a aplicação com configurações de banco de dados, autenticação JWT
    e endpoints RESTful. Configura o Flask-SQLAlchemy, Flask-Migrate e Flask-JWT-Extended,
    além de registrar os recursos da API.

    Returns:
        Flask: Instância configurada da aplicação Flask.
    """

    app = Flask(__name__)
    api = Api(app)

    # Configurações do banco de dados e JWT
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DB_URI']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY']

    # Inicializa o SQLAlchemy com a aplicação
    db.init_app(app)

    # Configura o gerenciador de tokens JWT
    jwt = JWTManager(app) 

    @jwt.invalid_token_loader
    def invalid_jwt(error):
        """
        Manipula erros de token JWT inválido.

        Retorna uma mensagem de erro e status HTTP 401 quando o token fornecido
        é inválido.

        Returns:
            tuple: Mensagem de erro e código de status 401.
        """
        return({
            "message": "Token de acesso inválido"},
            401
            )
    
    @jwt.unauthorized_loader
    def unauthorized_jwt(error):
        """
        Manipula erros de ausência de token JWT ou token não autorizado.

        Retorna uma mensagem de erro e status HTTP 401 quando nenhum token válido
        é fornecido.

        Returns:
            tuple: Mensagem de erro e código de status 401.
        """
        return(
            {"message": "Sem autorização, por favor informe um token válido"},
            401
        )

    # Cria as tabelas do banco de dados no contexto da aplicação
    with app.app_context():
        db.create_all()

    # Configura o Flask-Migrate para gerenciamento de migrações
    Migrate(app, db)

    # Registra os recursos da API RESTful
    api.add_resource(PurchaseOrders, '/purchase_orders')
    api.add_resource(PurchaseOrdersById, '/purchase_orders/<int:id>')
    api.add_resource(PurchaseOrdersItems, '/purchase_orders/<int:id>/items')
    api.add_resource(UserCreation, '/users')
    api.add_resource(UserLogin, '/login')

    return app
