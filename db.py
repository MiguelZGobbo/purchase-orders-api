"""Inicialização do objeto SQLAlchemy para interação com o banco de dados."""

from flask_sqlalchemy import SQLAlchemy

# Instância global do SQLAlchemy para ser usada em toda a aplicação
db = SQLAlchemy()