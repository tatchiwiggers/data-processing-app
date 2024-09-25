import streamlit as st
import snowflake.connector
import pandas as pd
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Streamlit title
st.title("Snowflake Data Viewer")

# Function to get data from Snowflake
def get_data_from_snowflake():
    conn_params = {
        'user': os.getenv("SNOWFLAKE_USER"),
        'password': os.getenv("SNOWFLAKE_PASSWORD"),
        'account': os.getenv("SNOWFLAKE_ACCOUNT"),
        'database': os.getenv("SNOWFLAKE_DATABASE"),
        'warehouse': os.getenv("SNOWFLAKE_WAREHOUSE"),
        'schema': os.getenv("SNOWFLAKE_SCHEMA")
    }

    try:
        # Connect to Snowflake
        conn = snowflake.connector.connect(**conn_params)
        cur = conn.cursor()

        # Query to retrieve data
        query = "SELECT * FROM ECOMMERCE_DB.DBT_TWIGGERS.STG_SCRAPED_PRODUCTS;"
        cur.execute(query)

        # Fetch data and load into a DataFrame
        data = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        df = pd.DataFrame(data, columns=columns)

        return df

    finally:
        # Ensure that the cursor and connection are closed
        cur.close()
        conn.close()

# Add a button in Streamlit to trigger data retrieval
if st.button('Load Data'):
    df = get_data_from_snowflake()

    if not df.empty:
        st.write("Data loaded successfully!")
        # Display the DataFrame in Streamlit
        st.dataframe(df)
    else:
        st.write("No data found.")

# Run the Streamlit app with: `streamlit run your_script.py`
