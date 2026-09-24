from pathlib import Path

from flask_migrate import upgrade
from sqlalchemy import inspect, text

from app import create_app
from db import db
from scripts.seed import seed
from users.model import UserModel


def test_upgrade_builds_schema_from_empty_database(tmp_path, monkeypatch):
    database = tmp_path / 'new.db'
    monkeypatch.setenv('DB_URI', f'sqlite:///{database.as_posix()}')
    monkeypatch.setenv('JWT_SECRET_KEY', 'migration-test-secret')
    app = create_app()

    with app.app_context():
        assert inspect(db.engine).get_table_names() == []

        upgrade(directory=str(Path(__file__).resolve().parents[1] / 'migrations'))

        schema = inspect(db.engine)
        assert set(schema.get_table_names()) == {
            'alembic_version',
            'purchase_orders',
            'purchase_orders_items',
            'users',
        }
        order_columns = {
            column['name']: column['nullable'] for column in schema.get_columns('purchase_orders')
        }
        item_columns = {
            column['name']: column['nullable']
            for column in schema.get_columns('purchase_orders_items')
        }
        assert order_columns['quantity'] is False
        assert item_columns['quantity'] is False
        assert db.session.execute(text('SELECT version_num FROM alembic_version')).scalar_one() == (
            '7b134dfa54cd'
        )


def test_seed_upgrades_empty_database(tmp_path, monkeypatch):
    database = tmp_path / 'seed.db'
    monkeypatch.setenv('DB_URI', f'sqlite:///{database.as_posix()}')
    monkeypatch.setenv('JWT_SECRET_KEY', 'migration-test-secret')

    seed()

    app = create_app()
    with app.app_context():
        assert db.session.execute(text('SELECT version_num FROM alembic_version')).scalar_one() == (
            '7b134dfa54cd'
        )


def test_upgrade_keeps_users_created_before_the_users_revision(tmp_path, monkeypatch):
    database = tmp_path / 'older.db'
    monkeypatch.setenv('DB_URI', f'sqlite:///{database.as_posix()}')
    monkeypatch.setenv('JWT_SECRET_KEY', 'migration-test-secret')
    app = create_app()

    with app.app_context():
        migrations = str(Path(__file__).resolve().parents[1] / 'migrations')
        upgrade(directory=migrations, revision='f606aa9493f1')
        UserModel.__table__.create(db.engine)
        db.session.execute(
            text("INSERT INTO users (email, password) VALUES ('existing@example.com', 'hash')")
        )
        db.session.commit()

        upgrade(directory=migrations)

        assert db.session.execute(text('SELECT email FROM users')).scalar_one() == (
            'existing@example.com'
        )
