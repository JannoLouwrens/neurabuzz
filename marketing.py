# marketing.py
import requests
import json
from time import sleep
from config import (OPENAI_API_KEY, FACEBOOK_ACCESS_TOKEN, FACEBOOK_APP_ID, 
                    FACEBOOK_APP_SECRET, FACEBOOK_AD_ACCOUNT_ID, FACEBOOK_PAGE_ID,
                    SHOPIFY_API_KEY, SHOPIFY_PASSWORD, SHOPIFY_STORE_URL, SHOPIFY_API_VERSION)

from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adcreative import AdCreative

def generate_ad_copy(product_title):
    prompt = f"Write a catchy and persuasive Facebook ad copy for a product called '{product_title}' that highlights its unique features."
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": "text-davinci-003",  # Replace with gpt-4 if available.
        "prompt": prompt,
        "max_tokens": 50
    }
    response = requests.post("https://api.openai.com/v1/completions", headers=headers, json=data)
    if response.status_code == 200:
        ad_copy = response.json()["choices"][0]["text"].strip()
        return ad_copy
    else:
        return "Discover this amazing product now!"

def generate_ad_image(product_title):
    # Return a placeholder image URL; replace with DALL·E API integration if desired.
    return "https://via.placeholder.com/1024x1024.png?text=" + product_title.replace(" ", "+")

def create_facebook_ad(product):
    # Initialize the Facebook API
    FacebookAdsApi.init(FACEBOOK_APP_ID, FACEBOOK_APP_SECRET, FACEBOOK_ACCESS_TOKEN)
    ad_account = AdAccount(FACEBOOK_AD_ACCOUNT_ID)
    
    # Generate ad copy and image
    ad_copy = generate_ad_copy(product["title"])
    ad_image_url = generate_ad_image(product["title"])
    print(f"Generating ad for product: {product['title']}")
    print(f"Ad Copy: {ad_copy}")
    print(f"Ad Image URL: {ad_image_url}")
    
    # Retrieve supplier URL from metafields if available
    supplier_url = ""
    if "metafields" in product:
        for meta in product["metafields"]:
            if meta.get("key") == "supplier_url":
                supplier_url = meta.get("value")
                break

    ad_creative_params = {
        'name': f"Creative for {product['title']}",
        'object_story_spec': {
            'page_id': FACEBOOK_PAGE_ID,
            'link_data': {
                'image_url': ad_image_url,
                'link': supplier_url,  # Use supplier URL if available.
                'message': ad_copy,
            }
        }
    }
    try:
        ad_creative = ad_account.create_ad_creative(params=ad_creative_params)
        print(f"Created ad creative: {ad_creative.get('id')}")
        # In a complete system, you can extend this to create ad sets and ads.
    except Exception as e:
        print("Error creating ad creative:", e)

def get_shopify_products():
    url = f"https://{SHOPIFY_API_KEY}:{SHOPIFY_PASSWORD}@{SHOPIFY_STORE_URL}/admin/api/{SHOPIFY_API_VERSION}/products.json"
    response = requests.get(url)
    if response.status_code == 200:
        products = response.json().get("products", [])
        print(f"Fetched {len(products)} products from Shopify")
        return products
    else:
        print("Error fetching products:", response.text)
        return []

def run_marketing_for_all_products():
    products = get_shopify_products()
    for product in products:
        create_facebook_ad(product)
        sleep(1)  # Pause briefly to avoid rate limits

if __name__ == "__main__":
    run_marketing_for_all_products()
