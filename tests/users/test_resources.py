def test_create_user_does_not_return_password(test_client):
    response = test_client.post(
        '/users',
        json={'email': 'portfolio@example.com', 'password': 'strong-password'},
    )

    assert response.status_code == 200
    assert response.json['id'] is not None
    assert response.json['email'] == 'portfolio@example.com'
    assert 'password' not in response.json


def test_create_user_rejects_duplicate_email(test_client):
    payload = {'email': 'portfolio@example.com', 'password': 'strong-password'}
    test_client.post('/users', json=payload)

    response = test_client.post('/users', json=payload)

    assert response.status_code == 400
    assert response.json['message'] == (
        'Já existe um usuário cadastrado com o email: portfolio@example.com'
    )


def test_create_user_rejects_blank_credentials(test_client):
    response = test_client.post('/users', json={'email': '   ', 'password': ''})

    assert response.status_code == 400
    assert response.json['message'] == 'Email e senha não podem ficar vazios'


def test_login_returns_token_usable_on_protected_endpoint(test_client):
    test_client.post(
        '/users',
        json={'email': 'portfolio@example.com', 'password': 'strong-password'},
    )

    response = test_client.post(
        '/login',
        json={'email': 'portfolio@example.com', 'password': 'strong-password'},
    )

    assert response.status_code == 200
    token = response.json['access_token']
    protected_response = test_client.get(
        '/purchase_orders',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert protected_response.status_code == 200


def test_login_with_invalid_password_returns_unauthorized(test_client):
    test_client.post(
        '/users',
        json={'email': 'portfolio@example.com', 'password': 'strong-password'},
    )

    response = test_client.post(
        '/login',
        json={'email': 'portfolio@example.com', 'password': 'wrong-password'},
    )

    assert response.status_code == 401
    assert response.json['message'] == 'Usuário ou senha incorretos'


def test_purchase_orders_require_authentication(test_client):
    response = test_client.get('/purchase_orders')

    assert response.status_code == 401
    assert response.json['message'] == ('Sem autorização, por favor informe um token válido')


def test_purchase_orders_reject_invalid_token(test_client):
    response = test_client.get(
        '/purchase_orders',
        headers={'Authorization': 'Bearer invalid-token'},
    )

    assert response.status_code == 401
    assert response.json['message'] == 'Token de acesso inválido'
