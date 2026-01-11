# NeuraBuzz - Automated E-Commerce Marketing Bot

Hands-off e-commerce automation: discovers trending products, generates listings, and manages fulfillment through scheduled tasks.

**Author:** Janno Louwrens
**Created:** 2023

## Overview

NeuraBuzz automates the e-commerce workflow for drop-shipping and product curation:

1. **Product Discovery** - Scrapes trending products from marketplaces
2. **Listing Generation** - Automatically creates Shopify product listings
3. **Marketing Automation** - Scheduled campaigns for new products
4. **Order Fulfillment** - Webhook-based order processing

## Features

- **Scheduled Scraping** - APScheduler runs discovery every 24 hours
- **Shopify Integration** - Full REST API integration for product management
- **Flask Webhooks** - Receives Shopify order notifications
- **Rate Limiting** - Configurable delays to respect API limits
- **Threaded Architecture** - Webhook server runs alongside scheduler

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      NeuraBuzz                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │  Scheduler  │    │   Flask     │    │   Config    │     │
│  │ (APScheduler)│   │  Webhooks   │    │   (.env)    │     │
│  └──────┬──────┘    └──────┬──────┘    └─────────────┘     │
│         │                  │                                │
│         ▼                  ▼                                │
│  ┌─────────────┐    ┌─────────────┐                        │
│  │  Product    │    │   Order     │                        │
│  │  Discovery  │    │ Fulfillment │                        │
│  └──────┬──────┘    └─────────────┘                        │
│         │                                                   │
│         ▼                                                   │
│  ┌─────────────┐    ┌─────────────┐                        │
│  │   Shopify   │◄───│  Marketing  │                        │
│  │    API      │    │  Automation │                        │
│  └─────────────┘    └─────────────┘                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Project Structure

```
neurabuzz/
├── main.py              # Entry point with scheduler
├── config.py            # Configuration (API keys)
├── product_discovery.py # Scraping and product creation
├── marketing.py         # Marketing automation
├── fulfillment.py       # Order webhook handling
├── requirements.txt
└── README.md
```

## Installation

### Prerequisites
- Python 3.8+
- Shopify store with API access

### Setup

**Windows:**
```powershell
# Clone repository
git clone https://github.com/JannoLouwrens/neurabuzz.git
cd neurabuzz

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**macOS / Linux:**
```bash
# Clone repository
git clone https://github.com/JannoLouwrens/neurabuzz.git
cd neurabuzz

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file or set environment variables:

```bash
# Shopify credentials
export SHOPIFY_STORE_URL="your-store.myshopify.com"
export SHOPIFY_API_KEY="your-api-key"
export SHOPIFY_API_PASSWORD="your-api-password"
```

On Windows (PowerShell):
```powershell
$env:SHOPIFY_STORE_URL="your-store.myshopify.com"
$env:SHOPIFY_API_KEY="your-api-key"
$env:SHOPIFY_API_PASSWORD="your-api-password"
```

## Configuration

Edit `config.py` with your credentials:

```python
# Shopify configuration
SHOPIFY_API_KEY = "your_shopify_api_key"
SHOPIFY_PASSWORD = "your_shopify_api_password"
SHOPIFY_STORE_URL = "your_store.myshopify.com"
SHOPIFY_API_VERSION = "2023-01"

# Scraping settings
AMAZON_URL = "https://www.amazon.in/gp/bestsellers/electronics/"
SLEEP_TIME = 2  # Rate limiting
```

## Usage

### Start the Bot

```bash
python main.py
```

This will:
1. Run initial product discovery
2. Run initial marketing campaign
3. Start Flask webhook server on port 5000
4. Schedule 24-hour recurring tasks

### Components

**Product Discovery:**
```python
from product_discovery import run_product_discovery
run_product_discovery()  # Scrapes and adds products to Shopify
```

**Marketing:**
```python
from marketing import run_marketing_for_all_products
run_marketing_for_all_products()  # Runs campaigns for all products
```

## Webhook Setup

Configure Shopify to send order webhooks to:
```
http://your-server:5000/webhook/orders
```

The Flask app handles incoming order notifications for fulfillment processing.

## Scheduling

Uses APScheduler for background tasks:

| Task | Interval | Description |
|------|----------|-------------|
| Product Discovery | 24 hours | Scrapes and adds new products |
| Marketing | 24 hours | Runs campaigns for all products |

## Technologies

- **Python 3.8+**
- **APScheduler** - Background task scheduling
- **Flask** - Webhook server
- **BeautifulSoup4** - Web scraping
- **Requests** - HTTP client
- **Shopify REST API** - Product management

## Use Case

Designed for passive income e-commerce workflows:
1. Discover trending products automatically
2. Create Shopify listings without manual entry
3. Handle orders through webhooks
4. Scale with scheduled automation

## Limitations

- Basic scraping (no proxy rotation)
- Single marketplace source
- Manual fulfillment initiation
- No inventory sync

## Future Enhancements

- Multi-marketplace scraping (Amazon, eBay, AliExpress)
- Proxy rotation for scraping
- Automated fulfillment with supplier APIs
- Price monitoring and adjustment
- Inventory management

## Disclaimer

This tool is for educational purposes. Ensure compliance with:
- Website Terms of Service
- API rate limits
- Drop-shipping regulations
- E-commerce platform policies

## License

MIT License
