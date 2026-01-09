import requests
from bs4 import BeautifulSoup
import json
import time
import config

# Function to scrape Amazon for top products
def scrape_amazon():
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0"
    }
    url = "https://www.amazon.in/gp/bestsellers/electronics/"

    soup = BeautifulSoup(requests.get(url, headers=headers).content, "html.parser")

    products = []
    for book in soup.select("div#gridItemRoot"):
        title = book.select_one("a:not(:has(img))").text.strip()
        price = book.select_one(".a-color-price")
        price = price.text.strip() if price else "Not Available"  # Handling missing price
        
        # Manually creating the product details here
        # You would extract the actual information and then map it to your Shopify product attributes
        products.append({
            "title": title,
            "price": price,
            "description": f"This is the {title}, a high-quality product available at Amazon.",  # Description
            "vendor": "Amazon",  # Vendor name
            "product_type": "Electronics",  # Type/category of product
        })

    return products


# Function to add a product to Shopify using API keys and password from config
def add_product_to_shopify(product):
    shopify_url = f"https://{config.SHOPIFY_STORE_URL}/admin/api/{config.SHOPIFY_API_VERSION}/products.json"
    
    # Manually adding the product details for Shopify
    new_product_data = {
        "product": {
            "title": product["title"],
            "body_html": product["description"],
            "vendor": product["vendor"],
            "product_type": product["product_type"],
            "variants": [
                {
                    "option1": "Default",  # Variant name
                    "price": product["price"],  # Price of the product
                    "sku": product["title"].replace(" ", "_").upper()  # SKU based on title
                }
            ]
        }
    }

    # Send POST request to create the product in Shopify
    response = requests.post(shopify_url, json=new_product_data, auth=(config.SHOPIFY_API_KEY, config.SHOPIFY_PASSWORD))

    # Check the response status
    if response.status_code == 201:
        print(f"Product '{product['title']}' added successfully!")
        print(json.dumps(response.json(), indent=2))  # Pretty print the created product details
    else:
        print(f"Error adding product '{product['title']}': {response.status_code}")
        print(response.text)


# Main function to scrape Amazon and add the products to Shopify
def main():
    # Scrape Amazon for top products
    amazon_products = scrape_amazon()

    # Manually add the products to Shopify
    for product in amazon_products:
        add_product_to_shopify(product)
        time.sleep(config.SLEEP_TIME)  # Sleep to avoid hitting the server too quickly


# Run the main function
if __name__ == "__main__":
    main()
