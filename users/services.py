from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token
from .model import UserModel

from .model import UserModel
from .exceptions import UserAlreadyExistException, UserEmailOrPasswordInvalidException

class UserService():

    def create(self, **kwargs):
        
        user = UserModel.find_user_by_email(kwargs['email'])

        if user:
            raise UserAlreadyExistException('Já existe um usuário cadastrado com o email: {}'. format(kwargs['email']))
        
        new_user = UserModel(**kwargs)
        new_user.save()
        return new_user.as_dict()
    
    def login(self, **kwargs):
        
        user = UserModel.find_user_by_email(kwargs['email'])
        
        if user and pbkdf2_sha256.verify(kwargs['password'], user.password):
            token = create_access_token(identity = user.id)
            return {'access_token': token}
        
        raise UserEmailOrPasswordInvalidException('Usuário ou senha incorretos')