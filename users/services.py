"""Serviços para gerenciamento de usuários, incluindo criação e autenticação."""

from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token

from .model import UserModel
from .exceptions import UserAlreadyExistException, UserEmailOrPasswordInvalidException

class UserService():
    """
    Classe responsável por gerenciar a lógica de negócios para usuários.

    Fornece métodos para criação de novos usuários e autenticação com geração de
    token JWT, utilizando o modelo UserModel e validações específicas.
    """

    def create(self, **kwargs):
        """
        Cria um novo usuário com base nos dados fornecidos.

        Verifica se o email já está cadastrado e, caso não esteja, cria um novo
        usuário com a senha criptografada e retorna seus dados como dicionário.
        Levanta UserAlreadyExistException se o email já existir.

        Args:
            **kwargs: Dicionário contendo 'email' e 'password' do usuário.

        Returns:
            dict: Dados do usuário criado (id e email).

        Raises:
            UserAlreadyExistException: Se o email já estiver cadastrado.
        """
        
        user = UserModel.find_user_by_email(kwargs['email'])

        if user:
            raise UserAlreadyExistException('Já existe um usuário cadastrado com o email: {}'. format(kwargs['email']))
        
        new_user = UserModel(**kwargs)
        new_user.save()
        return new_user.as_dict()
    
    def login(self, **kwargs):
        """
        Realiza a autenticação de um usuário e gera um token JWT.

        Verifica se o email existe e se a senha fornecida é válida. Em caso de
        sucesso, retorna um token de acesso. Caso contrário, levanta
        UserEmailOrPasswordInvalidException.

        Args:
            **kwargs: Dicionário contendo 'email' e 'password' do usuário.

        Returns:
            dict: Dicionário contendo o token de acesso ('access_token').

        Raises:
            UserEmailOrPasswordInvalidException: Se o email ou senha forem inválidos.
        """
        
        user = UserModel.find_user_by_email(kwargs['email'])
        
        if user and pbkdf2_sha256.verify(kwargs['password'], user.password):
            token = create_access_token(identity = str(user.id))
            return {'access_token': token}
        
        raise UserEmailOrPasswordInvalidException('Usuário ou senha incorretos')