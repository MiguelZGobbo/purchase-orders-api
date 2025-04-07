import json

def test_get_items_purchase_order_id(test_client, seed_db):
    response = test_client.get('/purchase_orders/{}/items'.format(seed_db['purchase_order'].id))

    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['id'] == seed_db['items'].id
    assert response.json[0]['description'] == seed_db['items'].description
    assert response.json[0]['price'] == seed_db['items'].price

def test_get_items_purchase_order_id_not_found(test_client):
    id = 999
    response = test_client.get('/purchase_orders/{}/items'.format(id))

    assert response.status_code == 200
    assert response.json['message'] == 'Pedido de id:{} não encontrado!'.format(id)

def test_post_purchase_order_item(test_client):
    obj = {'id': 2, 'description': '', 'price': 10.40 }

    response = test_client.post(
        '/purchase_orders/1/items',
        data = json.dumps(obj),
        content_type = 'application/json'
    )
     
    assert response.status_code == 200
    assert response.json['id'] == 1
    assert len(response.json['items']) == 2
    assert response.json['items'][1]['id'] == obj['id']

def test_post_invalid_id(test_client):
    obj = {'description': '', 'price': 10.40 }

    response = test_client.post(
        '/purchase_orders/1/items',
        data = json.dumps(obj),
        content_type = 'application/json'
    )

    assert response.status_code == 400
    assert response.json['message']['id'] == 'Informe um ID válido!'

def test_post_invalid_description(test_client):
    obj = {'id': 2, 'price': 10.40 }

    response = test_client.post(
        '/purchase_orders/1/items',
        data = json.dumps(obj),
        content_type = 'application/json'
    )

    assert response.status_code == 400
    assert response.json['message']['description'] == 'Informe uma descrição válida!'

def test_post_invalid_price(test_client):
    obj = {'id': 2, 'description': ''}

    response = test_client.post(
        '/purchase_orders/1/items',
        data = json.dumps(obj),
        content_type = 'application/json'
    )

    assert response.status_code == 400
    assert response.json['message']['price'] == 'Informe um preço válido!'

def test_post_purchase_order_not_found(test_client):
    id = 999

    obj = {'id': 2, 'description': '', 'price': 10.40 }

    response = test_client.post(
        '/purchase_orders/{}/items'.format(id),
        data = json.dumps(obj),
        content_type = 'application/json'
    )

    assert response.json['message'] == 'Pedido de id:{} não encontrado'.format(id)