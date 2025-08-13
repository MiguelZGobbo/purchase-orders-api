"""Endpoints RESTful para criação e autenticação de usuários."""

from flask_restful import Resource, reqparse
from .services import UserService

class Base():
    """
    Classe base para os recursos de usuários.

    Define o parser de argumentos compartilhado e a instância do serviço
    UserService para ser utilizada pelos recursos de criação e login.
    """
    __service__ = UserService

    parser = reqparse.RequestParser()
    
    parser.add_argument(
        'email',
        type = str,
        required = True,
        help = 'Informe um email'
    )
    
    parser.add_argument(
        'password',
        type = str,
        required = True,
        help = 'Informe uma senha'
    )

class UserCreation(Resource, Base):
    """
    Recurso para criação de novos usuários.

    Exige um email e senha válidos no corpo da requisição POST.
    """
    def post(self):
        """
        Cria um novo usuário com base nos dados fornecidos.

        Chama o método create do UserService para processar a criação e retorna
        o resultado.

        Returns:
            dict: Dados do usuário criado ou mensagem de erro.
        """
        data = UserCreation.parser.parse_args()
        return self.__service__.create(self, **data)
    
class UserLogin(Resource, Base):
    """
    Recurso para autenticação de usuários.

    Exige um email e senha válidos no corpo da requisição POST para realizar o login.
    """
    
    def post(self): 
        """
        Realiza o login do usuário com base nos dados fornecidos.

        Chama o método login do UserService para autenticar o usuário e retorna
        o token de acesso ou uma mensagem de erro.

        Returns:
            dict: Token de acesso ou mensagem de erro.
        """
        data = UserCreation.parser.parse_args()
        return self.__service__.login(self, **data)
    