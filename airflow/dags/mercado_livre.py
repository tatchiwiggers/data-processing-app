from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import logging
import snowflake.connector
from typing import List
import os
from dotenv import load_dotenv
from app import WebScraper
from process_data import insert_product_data
import json
from schema import ProductData

load_dotenv()

# Snowflake connection configuration
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA")


def scrape_products(**context):
    url = "https://www.mercadolivre.com.br/ofertas"
    scraper = WebScraper()
    products = scraper.scrape_products(url)

    serialized_products = [product.dict() for product in products]

    logging.info(f"Scraped {len(products)} products.")
    context['ti'].xcom_push(key='products', value=json.dumps(serialized_products))
    return serialized_products


def insert_into_snowflake(**context):
    serialized_products = context['ti'].xcom_pull(key='products', task_ids='scrape_products')
    # products = [ProductData(json.loads(p)) for p in json.loads(serialized_products)]
    products = json.loads(serialized_products)
    if not products:
        print('CAIU NO IF NOT PRODUCTS')
        logging.error("No products were scraped. Exiting.")
        return

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
        for product in products:
            try:
                data = ProductData(
                    product_link=product['product_link'],
                    product_image=product['product_image'],
                    product_title=product['product_title'],
                    previous_price=product['previous_price'],
                    current_price=product['current_price'],
                    discount=product['discount'],
                    installments=product['installments'],
                    seller=product['seller'],
                )
                insert_product_data(cursor, data)
            except Exception as e:
                logging.error(f"Error inserting product data: {e}")
        conn.commit()

        logging.info(f"Successfully inserted {len(products)} products into Snowflake.")

    except Exception as e:
        logging.error(f"Error: {e}")
        conn.rollback()

    finally:
        cursor.close()
        conn.close()


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
        python_callable=scrape_products,
        provide_context=True,
    )

    insert_task = PythonOperator(
        task_id='insert_into_snowflake',
        python_callable=insert_into_snowflake,
        provide_context=True,
    )

    scrape_task >> insert_task
