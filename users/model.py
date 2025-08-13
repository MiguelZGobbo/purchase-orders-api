"""Modelo de dados para a entidade de usuários."""

from db import db
from passlib.hash import pbkdf2_sha256

class UserModel(db.Model):
    """Modelo que representa a tabela de usuários no banco de dados."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(100), nullable = False, unique = True)
    password = db.Column(db.String(300), nullable = False)

    def __init__(self, email, password):
        """
        Inicializa um novo usuário com email e senha criptografada.

        Args:
            email (str): Email do usuário, deve ser único.
            password (str): Senha do usuário, que será criptografada.
        """
        self.email = email
        self.password = pbkdf2_sha256.hash(password)

    def as_dict(self):
        """
        Converte os dados do usuário em um dicionário.

        Returns:
            dict: Dicionário contendo o id e o email do usuário.
        """
        return{
            'id': self.id,
            'email': self.email
        }
    
    @classmethod
    def find_user_by_email(cls, _email):
        """
        Busca um usuário pelo email no banco de dados.

        Args:
            _email (str): Email do usuário a ser buscado.

        Returns:
            UserModel: Instância do usuário encontrado ou None se não encontrado.
        """
        return cls.query.filter_by(email = _email).first()
    
    def save(self):
        """
        Salva o usuário no banco de dados.

        Adiciona o usuário à sessão do banco e confirma a transação.
        """
        db.session.add(self)
        db.session.commit()