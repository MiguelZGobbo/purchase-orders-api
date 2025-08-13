"""Exceções personalizadas para o gerenciamento de erros da aplicação."""

from werkzeug.exceptions import HTTPException


class QuantityException(HTTPException):
    """
    Exceção levantada quando a quantidade fornecida é inválida.

    Define o código HTTP 400 para indicar uma requisição inválida, geralmente
    associada a quantidades que excedem limites ou são inadequadas no contexto
    do pedido de compra.
    """
    code = 400