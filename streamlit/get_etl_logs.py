import streamlit as st
import pandas as pd
import numpy as np  # Directly import numpy
from io import BytesIO
import get_data_from_snowflake_db
from dotenv import load_dotenv
import os

load_dotenv()

conn_params = {
    'user': os.getenv("SNOWFLAKE_USER"),
    'password': os.getenv("SNOWFLAKE_PASSWORD"),
    'account': os.getenv("SNOWFLAKE_ACCOUNT"),
    'database': os.getenv("SNOWFLAKE_DATABASE"),
    'warehouse': os.getenv("SNOWFLAKE_WAREHOUSE"),
    'schema': os.getenv("SNOWFLAKE_SCHEMA")
}

def get_etl_logs():
    # Mocked data for the example
    data = {
        "Run Timestamp": pd.date_range(start="2023-01-01", periods=100, freq='D'),
        "Status": ["Success"] * 80 + ["Failed"] * 20,
        "Errors": [None] * 80 + ["Timeout"] * 10 + ["Connection Error"] * 10,
        "Scraping Time (secs)": np.random.uniform(5, 15, 100),  # Use np.random
        "Loading Time (secs)": np.random.uniform(3, 10, 100),   # Use np.random
        "Data Volume (records)": np.random.randint(15000, 19000, 100),  # Use np.random
    }
    return pd.DataFrame(data)
    # df = get_data_from_snowflake_db.get_data_from_snowflake(**conn_params)
    # st.write("Data from Snowflake DB:", pd.DataFrame(df))

def show_customizable_views_page():
    st.title("🔍 Customizable Views")

    # Fetch logs
    df = get_etl_logs()

    # Filters
    st.sidebar.subheader("Filters")
    selected_status = st.sidebar.selectbox("Filter by Status", options=["All", "Success", "Failed"])
    selected_date = st.sidebar.date_input("Filter by Date", [])

    # Apply filters
    if selected_status != "All":
        df = df[df["Status"] == selected_status]
    if selected_date:
        df = df[df["Run Timestamp"].isin(pd.to_datetime(selected_date))]

    # Show filtered data
    st.subheader("Filtered Logs")
    st.dataframe(df)

    # Downloadable Reports
    st.subheader("Downloadable Reports")

    def convert_df_to_csv(df):
        return df.to_csv(index=False).encode('utf-8')

    def convert_df_to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='ETL Logs')
        processed_data = output.getvalue()
        return processed_data

    csv = convert_df_to_csv(df)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='etl_logs.csv',
        mime='text/csv',
    )

    excel = convert_df_to_excel(df)
    st.download_button(
        label="Download data as Excel",
        data=excel,
        file_name='etl_logs.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
