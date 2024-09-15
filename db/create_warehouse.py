import snowflake.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# SQL to create warehouse
create_warehouse_sql = """
CREATE OR REPLACE WAREHOUSE ecommerce_wh
WITH WAREHOUSE_SIZE = 'XSMALL'
AUTO_SUSPEND = 300
AUTO_RESUME = TRUE;
"""


# Connect to Snowflake and run the command
def create_warehouse():
    conn = snowflake.connector.connect(
        user=os.environ('SNOWFLAKE_USER'),
        password=os.environ('SNOWFLAKE_PASSWORD'),
        account=os.environ('SNOWFLAKE_ACCOUNT'),
        warehouse=os.environ('WAREHOUSE'),
        database=os.environ('SNOWFLAKE_DATABASE'),
        schema=os.environ('SNOWFLAKE_SCHEMA'),
    )

    try:
        cursor = conn.cursor()
        cursor.execute(create_warehouse_sql)
        conn.commit()
        print("Warehouse created successfully!")
    except Exception as e:
        print(f"Error creating warehouse: {e}")
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    create_warehouse()
