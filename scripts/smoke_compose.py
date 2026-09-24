"""Executa um fluxo HTTP curto contra a API iniciada pelo Docker Compose."""

import json
import os
import time
import uuid
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

BASE_URL = os.getenv('API_BASE_URL', 'http://127.0.0.1:5000').rstrip('/')
REQUEST_TIMEOUT_SECONDS = 5
STARTUP_TIMEOUT_SECONDS = 60


def request(method, path, payload=None, token=None):
    headers = {'Content-Type': 'application/json'}
    if token:
        headers['Authorization'] = f'Bearer {token}'

    body = json.dumps(payload).encode('utf-8') if payload is not None else None
    http_request = Request(
        f'{BASE_URL}{path}',
        data=body,
        headers=headers,
        method=method,
    )

    try:
        response = urlopen(http_request, timeout=REQUEST_TIMEOUT_SECONDS)
    except HTTPError as error:
        response = error

    raw_body = response.read()
    parsed_body = json.loads(raw_body) if raw_body else None
    return response.status, parsed_body


def require_status(result, expected_status, operation):
    status, body = result
    if status != expected_status:
        raise RuntimeError(
            f'{operation}: esperado HTTP {expected_status}, recebido HTTP {status}: {body}'
        )
    return body


def wait_for_api():
    deadline = time.monotonic() + STARTUP_TIMEOUT_SECONDS
    while time.monotonic() < deadline:
        try:
            status, body = request('GET', '/health')
            if status == 200 and body.get('status') == 'healthy':
                return
        except (ConnectionError, URLError, TimeoutError, json.JSONDecodeError):
            pass
        time.sleep(1)

    raise RuntimeError(f'A API não ficou saudável em {STARTUP_TIMEOUT_SECONDS} segundos')


def run_smoke_test():
    wait_for_api()

    unique_id = uuid.uuid4().hex
    email = f'smoke-{unique_id}@example.com'
    password = f'Smoke-{unique_id}'

    user = require_status(
        request('POST', '/users', {'email': email, 'password': password}),
        200,
        'Cadastro de usuário',
    )
    if 'password' in user:
        raise RuntimeError('O cadastro retornou a senha na resposta')

    login = require_status(
        request('POST', '/login', {'email': email, 'password': password}),
        200,
        'Login',
    )
    token = login.get('access_token')
    if not token:
        raise RuntimeError('O login não retornou access_token')

    require_status(request('GET', '/purchase_orders'), 401, 'Proteção sem token')

    order = require_status(
        request(
            'POST',
            '/purchase_orders',
            {'description': 'Pedido de fumaça do Compose', 'quantity': 50},
            token,
        ),
        200,
        'Criação do pedido',
    )
    order_id = order['id']

    require_status(
        request('GET', f'/purchase_orders/{order_id}', token=token),
        200,
        'Consulta do pedido',
    )

    for quantity in (30, 20):
        require_status(
            request(
                'POST',
                f'/purchase_orders/{order_id}/items',
                {
                    'description': f'Item de fumaça {quantity}',
                    'price': 12.5,
                    'quantity': quantity,
                },
                token,
            ),
            200,
            f'Criação de item com quantidade {quantity}',
        )

    items = require_status(
        request('GET', f'/purchase_orders/{order_id}/items', token=token),
        200,
        'Consulta de itens',
    )
    if sum(item['quantity'] for item in items) != 50:
        raise RuntimeError('A soma dos itens não corresponde ao limite do pedido')

    overflow = require_status(
        request(
            'POST',
            f'/purchase_orders/{order_id}/items',
            {'description': 'Item excedente', 'price': 1, 'quantity': 1},
            token,
        ),
        400,
        'Rejeição de item acima do limite',
    )
    if overflow.get('message') != 'Você só pode adicionar mais 0 itens':
        raise RuntimeError(f'Mensagem inesperada para item excedente: {overflow}')

    print('Smoke test do Docker Compose concluído com sucesso.')


if __name__ == '__main__':
    run_smoke_test()
