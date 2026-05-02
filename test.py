import requests
import xml.etree.ElementTree as ET

ORDER_URL     = 'http://127.0.0.1:5000/place_order'
INVENTORY_URL = 'http://127.0.0.1:5001/update_inventory'
PAYMENT_URL   = 'http://127.0.0.1:5002/process_payment'

def print_response(label, response):
    print(f"\n--- {label} ---")
    print(f"Status Code: {response.status_code}")
    try:
        root = ET.fromstring(response.content)
        ET.indent(root)
        print(ET.tostring(root, encoding='unicode'))
    except ET.ParseError:
        print(response.text)

# Test 1: Valid order (product 101, quantity 2)
print("=" * 40)
print("TEST 1: Valid Order (Product 101, Qty 2)")
print("=" * 40)
order_xml = "<Order><ProductID>101</ProductID><Quantity>2</Quantity></Order>"
response = requests.post(ORDER_URL, data=order_xml, headers={'Content-Type': 'application/xml'})
print_response("Order Response", response)

# Test 2: Invalid order - insufficient stock (product 102, quantity 999)
print("\n" + "=" * 40)
print("TEST 2: Insufficient Stock (Product 102, Qty 999)")
print("=" * 40)
order_xml = "<Order><ProductID>102</ProductID><Quantity>999</Quantity></Order>"
response = requests.post(ORDER_URL, data=order_xml, headers={'Content-Type': 'application/xml'})
print_response("Order Response", response)

# Test 3: Direct inventory check
print("\n" + "=" * 40)
print("TEST 3: Direct Inventory Update (Product 101, Qty 1)")
print("=" * 40)
inv_xml = "<Order><ProductID>101</ProductID><Quantity>1</Quantity></Order>"
response = requests.post(INVENTORY_URL, data=inv_xml, headers={'Content-Type': 'application/xml'})
print_response("Inventory Response", response)

# Test 4: Direct payment check
print("\n" + "=" * 40)
print("TEST 4: Direct Payment (Amount 50)")
print("=" * 40)
pay_xml = "<Payment><Amount>50</Amount></Payment>"
response = requests.post(PAYMENT_URL, data=pay_xml, headers={'Content-Type': 'application/xml'})
print_response("Payment Response", response)

# Test 5: Invalid payment (negative amount)
print("\n" + "=" * 40)
print("TEST 5: Invalid Payment (Amount -10)")
print("=" * 40)
pay_xml = "<Payment><Amount>-10</Amount></Payment>"
response = requests.post(PAYMENT_URL, data=pay_xml, headers={'Content-Type': 'application/xml'})
print_response("Payment Response", response)

print("\n" + "=" * 40)
print("All tests complete!")
print("=" * 40)