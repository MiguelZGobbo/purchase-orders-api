from flask import Flask, jsonify, request

app = Flask(__name__)

purchase_orders = [
    {
        'id': 1,
        'description': 'Pedido compra 1',
        'items': [
            {
                'id': 1,
                'description': 'item pedido 1',
                'price': 29.99
            }
        ]
    }
]

@app.route("/")
def home():
    return "Tamo na net pai! Daqui pra frente é só pra tras :)"

@app.route('/purchase_orders')
def get_purchase_orders():
    return jsonify(purchase_orders)

@app.route('/purchase_orders/<int:id>')
def get_purchase_orders_by_id(id): 
    for po in purchase_orders: 
         if po["id"] == id:
             return jsonify(purchase_orders)
    return ("Id não encontrado")

@app.route('/purchase_orders', methods = ['POST'])
def create_purchase_order():
    request_data = request.get_json()
    purchase_order = {
        'id': request_data['id'],
        'description': request_data['description'],
        'items': []
    }

    purchase_orders.append(purchase_order)

    return jsonify(purchase_order)

@app.route('/purchase_orders/<int:id>/items')      
def get_purchase_orders_items(id):
    for po in purchase_orders:
        if po['id'] == id:
            return jsonify(po['items'])
        
    return ("Id não encontrado")
    
@app.route('/purchase_orders/<int:id>/items', methods = ['POST'])      
def create_purchase_orders_items(id):
    request_data = request.get_json()
    for po in purchase_orders:
        if po['id'] == id:
            po['items'].append({
                'id': request_data['id'],
                'description': request_data['description'],
                'price': request_data['price']
            })

            return jsonify(po)       
         
    return ("Id não encontrado")

app.run(port=5000)

