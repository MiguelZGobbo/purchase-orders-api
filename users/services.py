from typing import Any

from flask_jwt_extended import create_access_token
from passlib.hash import pbkdf2_sha256

from exceptions.exceptions import InvalidInputException

from .exceptions import UserAlreadyExistException, UserEmailOrPasswordInvalidException
from .model import UserModel


class UserService:
    @staticmethod
    def create(email: str, password: str) -> dict[str, Any]:
        email = email.strip()
        if not email or not password.strip():
            raise InvalidInputException('Email e senha não podem ficar vazios')

        user = UserModel.find_user_by_email(email)
        if user:
            raise UserAlreadyExistException(
                f'Já existe um usuário cadastrado com o email: {email}',
            )
        new_user = UserModel(email, password)
        new_user.save()
        return new_user.as_dict()

    @staticmethod
    def login(email: str, password: str) -> dict[str, Any]:
        user = UserModel.find_user_by_email(email)
        if user and pbkdf2_sha256.verify(password, user.password):
            token = create_access_token(identity=str(user.id))
            return {'access_token': token}
        raise UserEmailOrPasswordInvalidException('Usuário ou senha incorretos')
