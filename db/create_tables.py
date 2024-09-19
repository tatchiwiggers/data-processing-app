import snowflake.connector
import params

# SQL to create the `scraped_products` table
create_table_sql = """
CREATE OR REPLACE TABLE ecommerce.scraped_products (
    product_id INT AUTOINCREMENT, -- Unique product identifier
    product_link STRING NOT NULL, -- URL of the product
    product_image STRING,         -- URL of the product image
    product_title STRING,         -- Title of the product
    previous_price DECIMAL(10, 2),-- Previous price of the product
    current_price DECIMAL(10, 2), -- Current price of the product
    discount STRING,              -- Discount information
    installments STRING,          -- Installments information
    seller STRING,                -- Seller information
    PRIMARY KEY (product_id)
);
"""

# Connect to Snowflake and create the table
def create_table():
    try:
        # Establish a connection to Snowflake using parameters
        conn = snowflake.connector.connect(
            user=params.SNOWFLAKE_USER,
            password=params.SNOWFLAKE_PASSWORD,
            account=params.SNOWFLAKE_ACCOUNT
        )

        # Create a cursor object and set the context for the warehouse, database, and schema
        with conn.cursor() as cursor:
            # Set the warehouse
            cursor.execute(f"USE WAREHOUSE {params.WAREHOUSE}")

            # Set the database
            cursor.execute(f"USE DATABASE {params.SNOWFLAKE_DATABASE}")

            # Set the schema
            cursor.execute(f"USE SCHEMA {params.SNOWFLAKE_SCHEMA}")

            # Execute the SQL to create the table
            cursor.execute(create_table_sql)
            print("Table 'scraped_products' created successfully!")

    except snowflake.connector.errors.Error as e:
        print(f"Snowflake error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection
        if conn:
            conn.close()

if __name__ == "__main__":
    create_table()
