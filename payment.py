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

class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    status = db.Column(db.String(10))

@app.route('/')
def index():
    return Response("<status>Payment service is running!</status>", mimetype='application/xml')

@app.route('/process_payment', methods=['GET', 'POST'])
def process_payment():
    if request.method == 'GET':
        return Response("<status>Send a POST request with XML body to process a payment.</status>", mimetype='application/xml')

    root = ET.fromstring(request.data)
    amount = float(root.find('Amount').text)

    response = ET.Element('PaymentResponse')

    if amount > 0:
        status = 'Success'
    else:
        status = 'Failed'
        ET.SubElement(response, 'Message').text = 'Invalid amount'

    payment = Payment(amount=amount, status=status)
    db.session.add(payment)
    db.session.commit()

    ET.SubElement(response, 'Status').text = status

    return Response(ET.tostring(response), mimetype='application/xml')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5002)