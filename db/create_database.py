import snowflake.connector
import os
import params

# Snowflake connection configuration
# SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
# SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
# SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")

print(params.SNOWFLAKE_ACCOUNT)
# SQL to create database
create_database_sql = f"""
CREATE OR REPLACE DATABASE {params.SNOWFLAKE_DATABASE}
COMMENT = 'Database for E-commerce product and sales data'
DATA_RETENTION_TIME_IN_DAYS = 1;
"""


# Connect to Snowflake and run the command
def create_database():
    conn = snowflake.connector.connect(
        user=params.SNOWFLAKE_USER,
        password=params.SNOWFLAKE_PASSWORD,
        account=params.SNOWFLAKE_ACCOUNT
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
