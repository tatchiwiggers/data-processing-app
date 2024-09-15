import snowflake.connector
import os

# Snowflake connection configuration
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")

# SQL to create database
create_database_sql = """
CREATE OR REPLACE DATABASE ecommerce_db
COMMENT = 'Database for E-commerce product and sales data'
DATA_RETENTION_TIME_IN_DAYS = 1;
"""


# Connect to Snowflake and run the command
def create_database():
    conn = snowflake.connector.connect(
        user=SNOWFLAKE_USER, password=SNOWFLAKE_PASSWORD, account=SNOWFLAKE_ACCOUNT
    )

    try:
        cursor = conn.cursor()
        cursor.execute(create_database_sql)
        conn.commit()
        print("Database created successfully!")
    except Exception as e:
        print(f"Error creating database: {e}")
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    create_database()
