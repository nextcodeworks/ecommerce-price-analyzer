# 🛒 E-Commerce Data Scraper & Analyzer

A Python GUI application that scrapes product data, analyzes trends, and visualizes results.

![My Image](https://raw.githubusercontent.com/nextcodeworks/ecommerce-price-analyzer/main/image.png?v=2)


## Features
- Web scraping with BeautifulSoup
- Data organization with pandas
- Interactive charts (matplotlib)
- User-friendly Tkinter interface
- Multiple analysis views

## Installation
```bash
git clone https://github.com/yourusername/ecommerce-scraper.git
cd ecommerce-scraper
pip install -r requirements.txt
```

## Usage
1. Run python main.py
2. Click "Scrape Data"
3. Select analysis type:
- Price Distribution
- Price Trends
- Top Products
- Category Breakdown

## Edit these in ```main.py```:
```bash
SCRAPING_URL = "https://webscraper.io/test-sites/e-commerce/allinone"
PRODUCT_CARD_CLASS = "product-wrapper"
PRODUCT_NAME_CLASS = "title" 
PRODUCT_PRICE_CLASS = "price"
```
