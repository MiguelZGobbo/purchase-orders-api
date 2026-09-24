import pytest

from app import create_app


def test_create_app_requires_jwt_secret(monkeypatch):
    monkeypatch.delenv('JWT_SECRET_KEY', raising=False)

    with pytest.raises(RuntimeError, match='JWT_SECRET_KEY'):
        create_app()


def test_swagger_describes_registered_routes_and_jwt(test_client):
    response = test_client.get('/apispec_1.json')
    assert response.status_code == 200
    spec = response.json
    assert set(spec['paths']) == {
        '/',
        '/health',
        '/users',
        '/login',
        '/purchase_orders',
        '/purchase_orders/{id}',
        '/purchase_orders/{id}/items',
    }
    assert {path: set(methods) for path, methods in spec['paths'].items()} == {
        '/': {'get'},
        '/health': {'get'},
        '/users': {'post'},
        '/login': {'post'},
        '/purchase_orders': {'get', 'post'},
        '/purchase_orders/{id}': {'get'},
        '/purchase_orders/{id}/items': {'get', 'post'},
    }
    assert spec['securityDefinitions']['BearerAuth']['type'] == 'apiKey'
    assert spec['securityDefinitions']['BearerAuth']['name'] == 'Authorization'
    assert (
        'access_token'
        in spec['paths']['/login']['post']['responses']['200']['schema']['properties']
    )
    assert (
        'password'
        not in spec['paths']['/users']['post']['responses']['200']['schema']['properties']
    )
    for path in ('/', '/health', '/users', '/login'):
        for operation in spec['paths'][path].values():
            assert 'security' not in operation

    for path in ('/purchase_orders', '/purchase_orders/{id}', '/purchase_orders/{id}/items'):
        for operation in spec['paths'][path].values():
            assert operation['security'] == [{'BearerAuth': []}]
            assert '401' in operation['responses']

    expected_fields = {
        '/users': {'email', 'password'},
        '/login': {'email', 'password'},
        '/purchase_orders': {'description', 'quantity'},
        '/purchase_orders/{id}/items': {'description', 'price', 'quantity'},
    }
    for path, fields in expected_fields.items():
        operation = spec['paths'][path]['post']
        body = next(param for param in operation['parameters'] if param['in'] == 'body')
        assert body['required'] is True
        assert set(body['schema']['required']) == fields
        assert set(body['schema']['properties']) == fields
        assert '200' in operation['responses']
        assert '400' in operation['responses']

    for path in ('/purchase_orders/{id}', '/purchase_orders/{id}/items'):
        for operation in spec['paths'][path].values():
            assert any(
                param['in'] == 'path' and param['name'] == 'id' and param['type'] == 'integer'
                for param in operation['parameters']
            )
            assert '404' in operation['responses']


def test_swagger_ui_loads(test_client):
    response = test_client.get('/apidocs', follow_redirects=True)
    assert response.status_code == 200
    assert b'swagger' in response.data.lower()
