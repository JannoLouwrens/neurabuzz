import os
import requests
from bs4 import BeautifulSoup
import json
import time

# Replace with your credentials and store URL
store_url = os.getenv("SHOPIFY_STORE_URL", "your-store.myshopify.com")
api_key = os.getenv("SHOPIFY_API_KEY", "your-api-key")
api_password = os.getenv("SHOPIFY_API_PASSWORD", "your-api-password")

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
        
        # Adding extracted product info to the list
        products.append({
            "title": title,
            "price": price,
            "description": f"This is the {title}, a high-quality product available at Amazon.",  # Description
            "vendor": "Amazon",  # Vendor name
            "product_type": "Electronics",  # Type/category of product
        })

    return products

# Function to search for a product on AliExpress
def search_aliexpress(product_title):
    search_url = f"https://www.aliexpress.com/wholesale?SearchText={product_title.replace(' ', '+')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Find the first product listing
    product_link = soup.find("a", class_="item-title")
    if product_link:
        product_url = "https:" + product_link["href"]
        # Find the first image in the product listing
        product_image = soup.find("img", class_="picCore")["src"]
        return product_url, product_image
    return None, None

# Function to add a product to Shopify using API keys and password from config
def add_product_to_shopify(product):
    # Search for the product on AliExpress
    aliexpress_url, aliexpress_image = search_aliexpress(product["title"])

    # If product is found on AliExpress
    if aliexpress_url and aliexpress_image:
        # Prepare product details with AliExpress info
        new_product_data = {
            "product": {
                "title": product["title"],
                "body_html": f"{product['description']} <br> <a href='{aliexpress_url}'>Check it on AliExpress</a>",  # Link to AliExpress
                "vendor": product["vendor"],
                "product_type": product["product_type"],
                "variants": [
                    {
                        "option1": "Default",
                        "price": product["price"],
                        "sku": product["title"].replace(" ", "_").upper()
                    }
                ],
                "images": [
                    {
                        "src": aliexpress_image  # AliExpress image URL
                    }
                ]
            }
        }

        url = f"https://{store_url}/admin/api/2023-01/products.json"

        # Send POST request to create the product in Shopify
        response = requests.post(url, json=new_product_data, auth=(api_key, api_password))

        if response.status_code == 201:
            print(f"Product '{product['title']}' added successfully!")
            print(json.dumps(response.json(), indent=2))  # Pretty print the created product details
        else:
            print(f"Error adding product '{product['title']}': {response.status_code}")
            print(response.text)
    else:
        print(f"Product '{product['title']}' not found on AliExpress.")

# Main function to scrape Amazon and add the products to Shopify
def main():
    # Scrape Amazon for top products
    amazon_products = scrape_amazon()

    # Add the products to Shopify
    for product in amazon_products:
        add_product_to_shopify(product)
        time.sleep(1)  # Sleep to avoid hitting the server too quickly

# Run the main function
if __name__ == "__main__":
    main()
