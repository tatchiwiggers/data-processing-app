import snowflake.connector
import os
import logging
from dotenv import load_dotenv
from app import WebScraper
from typing import List
from schema import (
    ProductData,
)

# Load environment variables
load_dotenv()

# Snowflake connection configuration
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA")


# Function to insert product data into Snowflake
def insert_product_data(cursor, product_data: ProductData):
    insert_query = """
    INSERT INTO ecommerce_db.raw_data.raw_scraped_data_source (
        product_link, product_image, product_title, previous_price, current_price, discount, installments, seller
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """
    cursor.execute(
        insert_query,
        (
            product_data.product_link,
            product_data.product_image,
            product_data.product_title,
            convert_price(product_data.previous_price),
            convert_price(product_data.current_price),
            product_data.discount,
            product_data.installments,
            product_data.seller,
        ),
    )


# Helper function to convert price string to decimal
def convert_price(price_str):
    if price_str:
        price_str = (
            price_str.replace("R$", "").replace(".", "").replace(",", ".").strip()
        )
        return float(price_str)
    return None


# Main function to scrape and insert products into Snowflake
def main():
    url = "https://www.mercadolivre.com.br/ofertas"

    # Create scraper instance and scrape products
    scraper = WebScraper()
    products: List[ProductData] = scraper.scrape_products(url)

    # Check if products were scraped
    if not products:
        logging.error("No products were scraped. Exiting.")
        return

    # Connect to Snowflake
    conn = snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=SNOWFLAKE_ACCOUNT,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA,
    )

    try:
        cursor = conn.cursor()

        # Insert each product into the database
        for product in products:
            insert_product_data(cursor, product)

        # Commit the transaction
        conn.commit()

        logging.info(f"Successfully inserted {len(products)} products into Snowflake.")

    except Exception as e:
        logging.error(f"Error: {e}")
        conn.rollback()

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    main()
