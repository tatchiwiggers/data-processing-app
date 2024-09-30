import streamlit as st
import pandas as pd
import numpy as np
from datetime import timedelta
from io import BytesIO
import random

# Function to generate the dataset with random times
def get_etl_logs():
    # Generate dates from 2024-09-21 to 2024-09-30 (10 days)
    start_date = pd.Timestamp('2024-09-21')
    end_date = pd.Timestamp('2024-09-30')
    date_range = pd.date_range(start=start_date, end=end_date)

    # Repeat the dates twice (once for "Success" and once for "Failed")
    repeated_dates = np.tile(date_range, 10)  # 10 repetitions (for 100 entries)

    # Add random times to the dates
    def add_random_time(date):
        random_time = timedelta(
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59),
            seconds=random.randint(0, 59)
        )
        return date + random_time

    # Apply random time to each date
    random_timestamps = [add_random_time(pd.Timestamp(date)) for date in repeated_dates]

    # Status array: First 80 "Success" and then 20 "Failed"
    status = ["Success"] * 80 + ["Failed"] * 20

    # Errors: None for "Success", and different errors for "Failed"
    errors = [None] * 80 + ["Timeout"] * 10 + ["Connection Error"] * 10

    # Scraping Time (secs) and Loading Time (secs): Fixed random values
    np.random.seed(42)  # Set a seed for reproducibility
    scraping_time = np.random.uniform(5, 15, 100)
    loading_time = np.random.uniform(3, 10, 100)

    # Data Volume (records): Fixed random integer values
    data_volume = np.random.randint(100, 220, 100)

    # Create DataFrame
    data = {
        "Run Timestamp": random_timestamps,
        "Status": status,
        "Errors": errors,
        "Scraping Time (secs)": scraping_time,
        "Loading Time (secs)": loading_time,
        "Data Volume (records)": data_volume,
    }

    return pd.DataFrame(data)

# Streamlit app
def show_customizable_views_page():
    st.title("🔍 Customizable Views")

    # Check if the dataset is already generated (using session state to keep it persistent)
    if 'etl_logs' not in st.session_state:
        # Generate the dataset once and store it in session state
        st.session_state.etl_logs = get_etl_logs()

    # Fetch logs from session state (so it does not randomize on every run)
    df = st.session_state.etl_logs

    # Sidebar filters
    st.sidebar.subheader("Filters")

    # Status filter (static key)
    selected_status = st.sidebar.selectbox(
        "Filter by Status",
        options=["All", "Success", "Failed"],
        key="status_selectbox"  # Static key to maintain selection
    )

    # Date range filter (static key)
    selected_date_range = st.sidebar.date_input(
        "Filter by Date Range",
        value=[pd.to_datetime("2024-09-21"), pd.to_datetime("2024-09-30")],
        key="date_range_input"  # Static key to maintain selection
    )

    # Apply status filter
    if selected_status != "All":
        df = df[df["Status"] == selected_status]

    # Apply date range filter
    if selected_date_range and len(selected_date_range) == 2:
        start_date, end_date = selected_date_range
        df = df[(df["Run Timestamp"] >= pd.to_datetime(start_date)) & (df["Run Timestamp"] <= pd.to_datetime(end_date))]

    # Show filtered data in the app
    st.subheader("Filtered ETL Logs")
    st.dataframe(df)

    # Downloadable Reports
    st.subheader("Downloadable Reports")

    # Convert dataframe to CSV
    def convert_df_to_csv(df):
        return df.to_csv(index=False).encode('utf-8')

    # Convert dataframe to Excel
    def convert_df_to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Filtered ETL Logs')
        processed_data = output.getvalue()
        return processed_data

    # CSV Download button
    csv = convert_df_to_csv(df)
    st.download_button(
        label="Download filtered data as CSV",
        data=csv,
        file_name='filtered_etl_logs.csv',
        mime='text/csv',
        key="csv_download"
    )

    # Excel Download button
    excel = convert_df_to_excel(df)
    st.download_button(
        label="Download filtered data as Excel",
        data=excel,
        file_name='filtered_etl_logs.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        key="excel_download"
    )
