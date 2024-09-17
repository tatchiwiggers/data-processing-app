import snowflake.connector

conn = snowflake.connector.connect(
    user='tatchiwiggers',
    password='Porcupine2406@',
    account='eikqune-ha60087',
    database='ECOMMERCE_DB',
    schema='PUBLIC'
)
print("Connected to Snowflake!")
conn.close()

# poetry run python sf_test.py
