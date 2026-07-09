"""Configurações e fixtures globais para os testes da aplicação."""

import os

import pytest
from flask_jwt_extended import create_access_token

from app import create_app


@pytest.fixture(scope='module')
def get_headers():
    """
    Fornece cabeçalhos de autenticação para os testes.

    Gera um token JWT para o usuário 'user_test' e retorna um dicionário com o
    cabeçalho de autorização no formato Bearer, reutilizável em testes que
    requerem autenticação.
    """
    token = create_access_token(identity='user_test')

    return {'Authorization': f'Bearer {token}'}


@pytest.fixture(scope='module', autouse=True)
def app_env():
    """
    Configura variáveis de ambiente necessárias para os testes.

    Define um banco SQLite em memória para isolar os testes do banco de
    desenvolvimento/produção.
    """
    os.environ['DB_URI'] = 'sqlite:///test.db'


@pytest.fixture(scope='module')
def test_client(app_env):
    """
    Fornece um cliente de teste para a aplicação Flask.

    Cria uma instância da aplicação Flask usando a função create_app e configura
    um cliente de teste no contexto da aplicação, garantindo que o ambiente esteja
    pronto para realizar requisições HTTP nos testes.
    """
    client = create_app()

    with client.test_client() as testing_client:
        with client.app_context():
            yield testing_client
