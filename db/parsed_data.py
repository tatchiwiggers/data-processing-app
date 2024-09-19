# import necessary packages
import snowflake.connector
import logging
import json
import os
import requests
from bs4 import BeautifulSoup
from typing import List
# from src.webscraping-ml import ProductData  # Ensure ProductData matches Snowflake schema
import params

from pydantic import BaseModel


class WebDriverConfig(BaseModel):
    driver_path: str
    headless: bool = False


class ProductData(BaseModel):
    product_link: str
    product_image: str
    product_title: str
    previous_price: str
    current_price: str
    discount: str
    installments: str
    seller: str



# Snowflake Insert Function
def insert_scraped_data(data: ProductData):
    try:
        # Establish connection to Snowflake
        conn = snowflake.connector.connect(
            user=params.SNOWFLAKE_USER,
            password=params.SNOWFLAKE_PASSWORD,
            account=params.SNOWFLAKE_ACCOUNT,
            warehouse=params.WAREHOUSE,
            database=params.SNOWFLAKE_DATABASE,
            schema=params.SNOWFLAKE_SCHEMA
        )

        # Clean price fields
        current_price = clean_price(data.current_price)
        previous_price = clean_price(data.previous_price)

        # Insert query
        insert_query = """
        INSERT INTO ecommerce.scraped_products (
            product_link, product_image, product_title,
            previous_price, current_price, discount,
            installments, seller
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """

        # Values to insert
        values = (
            data.product_link,
            data.product_image,
            data.product_title,
            previous_price,
            current_price,
            data.discount,
            data.installments,
            data.seller
        )

        # Execute the insert query
        with conn.cursor() as cursor:
            cursor.execute(insert_query, values)
            print("Data inserted successfully into 'scraped_products' table.")

    except snowflake.connector.errors.Error as e:
        print(f"Snowflake error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

# Helper function to clean price
def clean_price(price_str: str):
    if not price_str or price_str == "":
        return None
    return float(price_str.replace('R$', '').replace(',', '').strip())

# WebScraper class (unchanged)
class WebScraper:
    def get_html(self, url: str):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logging.error(f"Error fetching URL {url}: {e}")
            return None

    def scrape_products(self, url: str) -> List[ProductData]:
        products = []
        html = self.get_html(url)

        if not html:
            return products

        soup = BeautifulSoup(html, "html.parser")
        promotion_items = soup.find_all(class_="promotion-item")

        for item in promotion_items:
            try:
                product_link = item.find(class_="promotion-item__link-container")["href"]
                product_image = item.find(class_="promotion-item__img")["src"]
                product_title = item.find(class_="promotion-item__title").text.strip()
                previous_price = item.find(class_="andes-money-amount--previous").text.strip() if item.find(class_="andes-money-amount--previous") else ""
                current_price = item.find(class_="andes-money-amount--cents-superscript").text.strip()
                discount = item.find(class_="promotion-item__discount-text").text.strip() if item.find(class_="promotion-item__discount-text") else ""
                installments = item.find(class_="promotion-item__installments").text.strip() if item.find(class_="promotion-item__installments") else ""
                seller = item.find(class_="promotion-item__seller").text.strip() if item.find(class_="promotion-item__seller") else ""

                data = ProductData(
                    product_link=product_link,
                    product_image=product_image,
                    product_title=product_title,
                    previous_price=previous_price,
                    current_price=current_price,
                    discount=discount,
                    installments=installments,
                    seller=seller,
                )
                products.append(data)
            except Exception as e:
                logging.error(f"Error extracting product data: {e}")

        return products

# Main function to scrape and insert data
if __name__ == "__main__":
    url = "https://www.mercadolivre.com.br/ofertas"
    scraper = WebScraper()

    # Scrape products from the webpage
    products = scraper.scrape_products(url)
    logging.info(f"Scraped {len(products)} products.")

    # Insert scraped data into Snowflake
    if products:
        for product in products:
            insert_scraped_data(product)
            logging.info(f"Inserted product: {product.product_title}")
