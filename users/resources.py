from flask_restful import Resource, reqparse

from .services import UserService


class Base:
    __service__ = UserService

    parser = reqparse.RequestParser()
    parser.add_argument(
        'email',
        type=str,
        required=True,
        help='Informe um email',
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help='Informe uma senha',
    )


class UserCreation(Resource, Base):
    def post(self):
        """Cadastra um usuário.
        ---
        consumes: [application/json]
        parameters:
          - in: body
            name: user
            required: true
            schema:
              type: object
              required: [email, password]
              properties:
                email: {type: string}
                password: {type: string, format: password}
        responses:
          200:
            description: Usuário cadastrado, sem a senha.
            schema:
              type: object
              properties:
                id: {type: integer}
                email: {type: string}
          400:
            description: Dados inválidos ou email já cadastrado.
            schema:
              type: object
              properties:
                message: {type: string}
        """
        data = UserCreation.parser.parse_args()
        return self.__service__.create(data['email'], data['password'])


class UserLogin(Resource, Base):
    def post(self):
        """Autentica um usuário e retorna um token JWT.
        ---
        consumes: [application/json]
        parameters:
          - in: body
            name: credentials
            required: true
            schema:
              type: object
              required: [email, password]
              properties:
                email: {type: string}
                password: {type: string, format: password}
        responses:
          200:
            description: Token para usar no cabeçalho Authorization.
            schema:
              type: object
              properties:
                access_token: {type: string}
          400:
            description: Email ou senha não informados.
            schema:
              type: object
              properties:
                message: {type: object}
          401:
            description: Credenciais incorretas.
            schema:
              type: object
              properties:
                message: {type: string}
        """
        data = UserCreation.parser.parse_args()
        return self.__service__.login(data['email'], data['password'])
