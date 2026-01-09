# fulfillment.py
from flask import Flask, request, jsonify
import json
from config import ALIEXPRESS_API_KEY

app = Flask(__name__)

def place_aliexpress_order(supplier_url, customer_info):
    # Dummy function: Replace with actual API calls or Selenium automation for AliExpress order placement.
    print("Placing order on AliExpress for supplier URL:", supplier_url)
    print("Customer Info:", customer_info)
    # Simulate order placement
    return {"status": "order_placed", "order_id": "ALEX123456"}

@app.route('/shopify/order_webhook', methods=['POST'])
def shopify_order_webhook():
    data = request.get_json()
    print("Received Shopify order webhook:", data)
    try:
        order_id = data.get("id")
        line_items = data.get("line_items", [])
        customer = data.get("customer", {})
        customer_info = {
            "name": f"{customer.get('first_name', '')} {customer.get('last_name', '')}",
            "email": customer.get("email", ""),
            "address": data.get("shipping_address", {})
        }
        for item in line_items:
            metafields = item.get("metafields", [])
            supplier_url = None
            for meta in metafields:
                if meta.get("key") == "supplier_url":
                    supplier_url = meta.get("value")
                    break
            if supplier_url:
                result = place_aliexpress_order(supplier_url, customer_info)
                print(f"Order fulfillment result for order {order_id}:", result)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print("Error processing order:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    # Run on port 5000; use a tool like ngrok to expose externally for Shopify.
    app.run(host='0.0.0.0', port=5000, debug=True)
