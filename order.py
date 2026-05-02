from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import xml.etree.ElementTree as ET
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@127.0.0.1/order_system'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
db.init_app(app)
CORS(app)

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(10))
    quantity = db.Column(db.Integer)
    total_amount = db.Column(db.Float)

INVENTORY_URL = 'http://127.0.0.1:5001/update_inventory'
PAYMENT_URL   = 'http://127.0.0.1:5002/process_payment'

@app.route('/')
def index():
    return Response("<status>Order service is running!</status>", mimetype='application/xml')

@app.route('/place_order', methods=['GET', 'POST'])
def place_order():
    if request.method == 'GET':
        return Response("<status>Send a POST request with XML body to place an order.</status>", mimetype='application/xml')

    root = ET.fromstring(request.data)
    product_id = root.find('ProductID').text
    quantity = int(root.find('Quantity').text)
    total_amount = float(root.find('TotalAmount').text)

    # Save order
    order = Order(product_id=product_id, quantity=quantity, total_amount=total_amount)
    db.session.add(order)
    db.session.commit()

    # Step 1: inventory
    inv_resp = requests.post(INVENTORY_URL, data=request.data,
                             headers={'Content-Type': 'application/xml'})

    inv_root = ET.fromstring(inv_resp.content)
    if inv_root.find('Status').text != 'Success':
        return Response(inv_resp.content, mimetype='application/xml')

    # Step 2: payment
    payment_xml = ET.Element('Payment')
    ET.SubElement(payment_xml, 'Amount').text = str(total_amount)

    pay_resp = requests.post(PAYMENT_URL, data=ET.tostring(payment_xml),
                             headers={'Content-Type': 'application/xml'})

    return Response(pay_resp.content, mimetype='application/xml')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5000)