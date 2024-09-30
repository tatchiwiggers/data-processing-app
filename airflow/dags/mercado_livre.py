import json
import logging
import os
from datetime import datetime
from typing import List

import snowflake.connector
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from dotenv import load_dotenv

from app import WebScraper
from process_data import insert_product_data
from schema import ProductData


load_dotenv()

# Snowflake connection configuration
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA")


# def scrape_products(**context):
#     url = "https://www.mercadolivre.com.br/ofertas"
#     scraper = WebScraper()
#     products = scraper.scrape_products(url)

#     serialized_products = [product.dict() for product in products]

#     logging.info(f"Scraped {len(products)} products.")
#     context['ti'].xcom_push(key='products', value=json.dumps(serialized_products))
#     return serialized_products


# def insert_into_snowflake(**context):
#     serialized_products = context['ti'].xcom_pull(key='products', task_ids='scrape_products')
#     # products = [ProductData(json.loads(p)) for p in json.loads(serialized_products)]
#     products = json.loads(serialized_products)
#     if not products:
#         print('CAIU NO IF NOT PRODUCTS')
#         logging.error("No products were scraped. Exiting.")
#         return

#     conn = snowflake.connector.connect(
#         user=SNOWFLAKE_USER,
#         password=SNOWFLAKE_PASSWORD,
#         account=SNOWFLAKE_ACCOUNT,
#         warehouse=SNOWFLAKE_WAREHOUSE,
#         database=SNOWFLAKE_DATABASE,
#         schema=SNOWFLAKE_SCHEMA,
#     )

#     try:
#         cursor = conn.cursor()
#         for product in products:
#             try:
#                 data = ProductData(
#                     product_link=product['product_link'],
#                     product_image=product['product_image'],
#                     product_title=product['product_title'],
#                     previous_price=product['previous_price'],
#                     current_price=product['current_price'],
#                     discount=product['discount'],
#                     installments=product['installments'],
#                     seller=product['seller'],
#                 )
#                 insert_product_data(cursor, data)
#             except Exception as e:
#                 logging.error(f"Error inserting product data: {e}")
#         conn.commit()

#         logging.info(f"Successfully inserted {len(products)} products into Snowflake.")

#     except Exception as e:
#         logging.error(f"Error: {e}")
#         conn.rollback()

#     finally:
#         cursor.close()
#         conn.close()

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


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 9, 22),
    'retries': 1,
}

with DAG(
    dag_id='mercadolivre_scraper_to_snowflake_dag',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
) as dag:

    scrape_task = PythonOperator(
        task_id='scrape_products',
        python_callable=main,
        provide_context=True,
    )

    # insert_task = PythonOperator(
    #     task_id='insert_into_snowflake',
    #     python_callable=insert_product_data,
    #     provide_context=True,
    # )

    scrape_task
