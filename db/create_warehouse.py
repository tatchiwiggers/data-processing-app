import snowflake.connector
import os
import params

# SQL to create warehouse
create_warehouse_sql = f"""
CREATE OR REPLACE WAREHOUSE {params.WAREHOUSE}
WITH WAREHOUSE_SIZE = 'XSMALL'
AUTO_SUSPEND = 300
AUTO_RESUME = TRUE;
"""

import snowflake.connector
import os
import params

# SQL to create warehouse with corrected syntax
create_warehouse_sql = f"""
CREATE OR REPLACE WAREHOUSE {params.WAREHOUSE}
WAREHOUSE_SIZE = 'XSMALL'
AUTO_SUSPEND = 300
AUTO_RESUME = TRUE;
"""

# Connect to Snowflake and run the command
def create_warehouse():
    try:
        # Establish a connection to Snowflake using parameters
        conn = snowflake.connector.connect(
            user=params.SNOWFLAKE_USER,
            password=params.SNOWFLAKE_PASSWORD,
            account=params.SNOWFLAKE_ACCOUNT,
            database=params.SNOWFLAKE_DATABASE,
            schema=params.SNOWFLAKE_SCHEMA
        )

        # Execute the SQL to create the warehouse
        with conn.cursor() as cursor:
            cursor.execute(create_warehouse_sql)
            print("Warehouse created successfully!")

    except snowflake.connector.errors.Error as e:
        print(f"Snowflake error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection
        if conn:
            conn.close()

if __name__ == "__main__":
    create_warehouse()
