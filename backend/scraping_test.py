from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import time

# Assign URL to scrape
url_to_scrape = "https://www.abercrombie.com/shop/us/mens"
# url_to_scrape = "https://www.abercrombie.com/shop/us/mens-bottoms--1"

# setup chrome webdriver
driver = webdriver.Chrome()

#load the web page
driver.get(url_to_scrape)

# Allow some time for initial page load
time.sleep(1)

# Scroll to the bottom of the page in increments
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down by one screen height
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Wait for content to load
    time.sleep(7)
    # Calculate new scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    # Check if we have reached the bottom of the page
    if new_height == last_height:
        break
    last_height = new_height

# Function to extract HTML document from the given URL
def getHTMLDocument(url):
    # Request for HTML document of the given URL
    response = requests.get(url)
    return response.text

# Create document
html_document = driver.page_source

# Create soup object
soup = BeautifulSoup(html_document, 'html.parser')

# Find all product cards
product_cards = soup.find_all('li', class_='catalog-productCard-module__productCard')

# Extract desired details
for card in product_cards:
    # Extract name
    name_tag = card.find('h2', {'data-aui': 'product-card-name'})
    name = name_tag.text if name_tag else "N/A"

    # Extract price
    price_tag = card.find('span', {'class': 'product-price-text'})
    price = price_tag.text if price_tag else "N/A"

    # Extract image
    img_tag = card.find('img', {'data-aui': 'product-card-image'})
    image_url = img_tag['src'] if img_tag else "N/A"

    # Extract product link
    link_tag = card.find('a', href=True)
    link = "https://www.abercrombie.com" + link_tag['href'] if link_tag else "N/A"

    # Print extracted details
    print(f"Name: {name}")
    print(f"Price: {price}")
    print(f"Image URL: {image_url}")
    print(f"Link: {link}")
    print("-" * 40)

print(len(product_cards))

driver.quit()