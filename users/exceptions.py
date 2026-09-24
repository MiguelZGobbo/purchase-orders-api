"""Exceções personalizadas para o gerenciamento de usuários."""

from werkzeug.exceptions import HTTPException


class UserAlreadyExistException(HTTPException):
    """
    Exceção levantada quando um email já está cadastrado.

    Define o código HTTP 400 para indicar uma requisição inválida.
    """

    code = 400


class UserEmailOrPasswordInvalidException(HTTPException):
    """
    Exceção levantada quando o email ou a senha fornecidos são inválidos.

    Define o código HTTP 401 para indicar que as credenciais de autenticação são inválidas.
    """

    code = 401
