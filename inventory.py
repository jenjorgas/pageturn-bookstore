import os
from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import xml.etree.ElementTree as ET

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'mysql+pymysql://root:@127.0.0.1/order_system')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
db.init_app(app)
CORS(app)

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(10), unique=True)
    stock = db.Column(db.Integer)

@app.route('/')
def index():
    return Response("<status>Inventory service is running!</status>", mimetype='application/xml')

@app.route('/update_inventory', methods=['GET', 'POST'])
def update_inventory():
    if request.method == 'GET':
        return Response("<status>Send a POST request with XML body to update inventory.</status>", mimetype='application/xml')

    root = ET.fromstring(request.data)
    product_id = root.find('ProductID').text
    quantity = int(root.find('Quantity').text)

    product = Product.query.filter_by(product_id=product_id).first()

    response = ET.Element('InventoryResponse')

    if product and product.stock >= quantity:
        product.stock -= quantity
        db.session.commit()
        ET.SubElement(response, 'Status').text = 'Success'
        ET.SubElement(response, 'RemainingStock').text = str(product.stock)
    else:
        ET.SubElement(response, 'Status').text = 'Failed'
        ET.SubElement(response, 'Message').text = 'Insufficient stock'

    return Response(ET.tostring(response), mimetype='application/xml')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not Product.query.first():
            db.session.add(Product(product_id='101', stock=10))
            db.session.add(Product(product_id='102', stock=5))
            db.session.add(Product(product_id='103', stock=5))
            db.session.add(Product(product_id='104', stock=0))
            db.session.add(Product(product_id='201', stock=18))
            db.session.add(Product(product_id='202', stock=9))
            db.session.add(Product(product_id='203', stock=4))
            db.session.add(Product(product_id='301', stock=14))
            db.session.add(Product(product_id='302', stock=8))
            db.session.add(Product(product_id='303', stock=0))
            db.session.add(Product(product_id='401', stock=20))
            db.session.add(Product(product_id='402', stock=6))
            db.session.add(Product(product_id='501', stock=22))
            db.session.add(Product(product_id='502', stock=11))
            db.session.add(Product(product_id='503', stock=0))
            db.session.add(Product(product_id='601', stock=10))
            db.session.add(Product(product_id='602', stock=15))
            db.session.add(Product(product_id='701', stock=6))
            db.session.add(Product(product_id='702', stock=3))
            db.session.commit()
    app.run(host='0.0.0.0', port=5001)