# main.py
import time
import threading
from apscheduler.schedulers.background import BackgroundScheduler
from product_discovery import run_product_discovery
from marketing import run_marketing_for_all_products
from fulfillment import app  # Import the Flask app

def scheduled_product_discovery():
    print("Scheduled Task: Running product discovery...")
    run_product_discovery()

def scheduled_marketing():
    print("Scheduled Task: Running marketing for all products...")
    run_marketing_for_all_products()

def run_flask_app():
    # Run the Flask app to catch Shopify webhooks
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == "__main__":
    # Initialize the background scheduler.
    scheduler = BackgroundScheduler()
    # Schedule product discovery to run every 24 hours.
    scheduler.add_job(scheduled_product_discovery, 'interval', hours=24)
    # Schedule marketing automation to run every 24 hours.
    scheduler.add_job(scheduled_marketing, 'interval', hours=24)
    scheduler.start()
    
    # Optionally, run tasks immediately on startup.
    scheduled_product_discovery()
    scheduled_marketing()
    
    # Run the Flask app in a separate thread for handling webhooks.
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.start()
    
    try:
        # Keep the main thread alive.
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
