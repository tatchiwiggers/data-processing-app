import snowflake.connector

# Test a basic connection (replace with your credentials)
conn = snowflake.connector.connect(
    user='tatchiwiggers',
    password='Porcupine2406@',
    account='https://eikqune-ha60087.snowflakecomputing.com'
)
print("Connected to Snowflake!")
conn.close()
