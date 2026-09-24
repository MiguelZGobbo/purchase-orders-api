"""Testes para os endpoints de itens de pedidos de compra."""

import json


def test_get_items_purchase_order_id(test_client, get_headers, seed_db):
    """
    Testa a recuperação de itens associados a um pedido de compra existente.

    Verifica se o endpoint GET /purchase_orders/{id}/items retorna status 200,
    um item na resposta e se os dados do item correspondem aos valores inseridos
    pela fixture seed_db.
    """
    po_id = seed_db['purchase_order'].id
    response = test_client.get(f'/purchase_orders/{po_id}/items', headers=get_headers)

    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['id'] == seed_db['items'].id
    assert response.json[0]['description'] == seed_db['items'].description
    assert response.json[0]['price'] == seed_db['items'].price
    assert response.json[0]['quantity'] == seed_db['items'].quantity


def test_get_items_purchase_order_id_not_found(test_client, get_headers):
    """
    Testa a recuperação de itens para um pedido de compra inexistente.

    Verifica se o endpoint GET /purchase_orders/{id}/items retorna status 200
    e uma mensagem indicando que o pedido não foi encontrado.
    """
    id = 999
    response = test_client.get(f'/purchase_orders/{id}/items', headers=get_headers)

    assert response.status_code == 404
    assert response.json['message'] == f'Pedido de id:{id} não encontrado!'


def test_post_purchase_order_item(test_client, get_headers, seed_db):
    """
    Testa a criação de um novo item para um pedido de compra existente.

    Verifica se o endpoint POST /purchase_orders/{id}/items retorna status 200,
    cria um item com ID não nulo e retorna os dados corretos do item criado.
    """
    obj = {'description': 'Item teste', 'price': 10.40, 'quantity': 5}

    response = test_client.post(
        '/purchase_orders/{}/items'.format(seed_db['purchase_order'].id),
        data=json.dumps(obj),
        content_type='application/json',
        headers=get_headers,
    )

    assert response.status_code == 200
    assert response.json['id'] is not None
    assert response.json['description'] == obj['description']
    assert response.json['price'] == obj['price']


def test_post_purchase_order_item_invalid_quantity(test_client, get_headers, seed_db):
    """
    Testa a criação de um item com quantidade que excede o limite do pedido.

    Verifica se o endpoint POST /purchase_orders/{id}/items retorna status 400
    e uma mensagem indicando que a quantidade máxima permitida foi excedida.
    """
    obj = {'description': 'Item teste', 'price': 10.40, 'quantity': 30}

    response = test_client.post(
        '/purchase_orders/{}/items'.format(seed_db['purchase_order'].id),
        data=json.dumps(obj),
        content_type='application/json',
        headers=get_headers,
    )

    assert response.status_code == 400
    assert response.json['message'] == 'Você só pode adicionar mais 20 itens'


def test_post_purchase_order_item_at_quantity_limit(test_client, get_headers, seed_db):
    purchase_order_id = seed_db['purchase_order'].id
    response = test_client.post(
        f'/purchase_orders/{purchase_order_id}/items',
        json={'description': 'Último item', 'price': 10, 'quantity': 20},
        headers=get_headers,
    )

    assert response.status_code == 200
    items_response = test_client.get(
        f'/purchase_orders/{purchase_order_id}/items',
        headers=get_headers,
    )
    assert sum(item['quantity'] for item in items_response.json) == 50

    overflow_response = test_client.post(
        f'/purchase_orders/{purchase_order_id}/items',
        json={'description': 'Excedente', 'price': 10, 'quantity': 1},
        headers=get_headers,
    )
    assert overflow_response.status_code == 400
    assert overflow_response.json['message'] == 'Você só pode adicionar mais 0 itens'


def test_post_invalid_quantity(test_client, get_headers, seed_db):
    """
    Testa a criação de um item com quantidade não informada.

    Verifica se o endpoint POST /purchase_orders/{id}/items retorna status 400
    e uma mensagem indicando que a quantidade fornecida é inválida.
    """
    obj = {'price': 10.40, 'description': 'Item teste'}

    response = test_client.post(
        '/purchase_orders/{}/items'.format(seed_db['purchase_order'].id),
        data=json.dumps(obj),
        content_type='application/json',
        headers=get_headers,
    )

    assert response.status_code == 400
    assert response.json['message']['quantity'] == 'Informe uma quantidade válida!'


def test_post_invalid_description(test_client, get_headers, seed_db):
    """
    Testa a criação de um item com descrição não informada.

    Verifica se o endpoint POST /purchase_orders/{id}/items retorna status 400
    e uma mensagem indicando que a descrição fornecida é inválida.
    """
    obj = {'price': 10.40, 'quantity': 5}

    response = test_client.post(
        '/purchase_orders/{}/items'.format(seed_db['purchase_order'].id),
        data=json.dumps(obj),
        content_type='application/json',
        headers=get_headers,
    )

    assert response.status_code == 400
    assert response.json['message']['description'] == 'Informe uma descrição válida!'


def test_post_invalid_price(test_client, get_headers, seed_db):
    """
    Testa a criação de um item com preço não informado.

    Verifica se o endpoint POST /purchase_orders/{id}/items retorna status 400
    e uma mensagem indicando que o preço fornecido é inválido.
    """
    obj = {'description': 'Item teste', 'quantity': 10}

    response = test_client.post(
        '/purchase_orders/{}/items'.format(seed_db['purchase_order'].id),
        data=json.dumps(obj),
        content_type='application/json',
        headers=get_headers,
    )

    assert response.status_code == 400
    assert response.json['message']['price'] == 'Informe um preço válido!'


def test_post_purchase_order_item_with_zero_quantity(test_client, get_headers, seed_db):
    """Deve rejeitar itens sem quantidade positiva."""
    response = test_client.post(
        f'/purchase_orders/{seed_db["purchase_order"].id}/items',
        json={'description': 'Item teste', 'price': 10.40, 'quantity': 0},
        headers=get_headers,
    )

    assert response.status_code == 400
    assert response.json['message'] == 'A quantidade deve ser maior que zero'


def test_post_purchase_order_item_with_negative_quantity(test_client, get_headers, seed_db):
    """Deve rejeitar quantidades negativas que reduziriam o total já utilizado."""
    response = test_client.post(
        f'/purchase_orders/{seed_db["purchase_order"].id}/items',
        json={'description': 'Item teste', 'price': 10.40, 'quantity': -10},
        headers=get_headers,
    )

    assert response.status_code == 400
    assert response.json['message'] == 'A quantidade deve ser maior que zero'


def test_post_purchase_order_item_with_negative_price(test_client, get_headers, seed_db):
    """Deve rejeitar preços negativos."""
    response = test_client.post(
        f'/purchase_orders/{seed_db["purchase_order"].id}/items',
        json={'description': 'Item teste', 'price': -1, 'quantity': 1},
        headers=get_headers,
    )

    assert response.status_code == 400
    assert response.json['message'] == 'Informe um preço válido!'


def test_post_purchase_order_item_with_blank_description(test_client, get_headers, seed_db):
    response = test_client.post(
        f'/purchase_orders/{seed_db["purchase_order"].id}/items',
        json={'description': '   ', 'price': 10, 'quantity': 1},
        headers=get_headers,
    )

    assert response.status_code == 400
    assert response.json['message'] == 'Informe uma descrição válida!'


def test_post_purchase_order_not_found(test_client, get_headers):
    """
    Testa a criação de um item para um pedido de compra inexistente.

    Verifica se o endpoint POST /purchase_orders/{id}/items retorna uma mensagem
    indicando que o pedido não foi encontrado.
    """
    id = 99999

    obj = {'description': 'Item teste', 'price': 10.40, 'quantity': 5}

    response = test_client.post(
        f'/purchase_orders/{id}/items',
        data=json.dumps(obj),
        content_type='application/json',
        headers=get_headers,
    )

    assert response.status_code == 404
    assert response.json['message'] == f'Pedido de id:{id} não encontrado'
