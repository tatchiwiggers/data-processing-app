import streamlit as st
import pandas as pd
import snowflake.connector
import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

# Function to gather metrics for each stage (replace mock data with real logic)
def get_web_scraping_metrics():
    return {
        'Number of Pages Scraped': 120,
        'Data Volume': '15,000 records',
        'Scraping Time': '10 minutes',
        'Success Rate': '98%',
    }

def get_data_parsing_metrics():
    return {
        'Parsing Success Rate': '95%',
        'Data Quality Metrics': '3 missing fields, 1 type error',
    }

def get_snowflake_loading_metrics():
    return {
        'Records Loaded': 14800,
        'Loading Time': '5 minutes',
        'Loading Errors': 'None',
    }

def get_dbt_transformation_metrics():
    return {
        'Transformation Success': 'Success',
        'Number of Models Processed': 10,
        'Transformation Time': '7 minutes',
        'Data Validation': 'All checks passed',
    }

def get_final_snowflake_metrics():
    return {
        'Records Processed': 14800,
        'Final Table Status': 'Healthy (data fresh, record counts match)',
    }

# Function to display a metric as a card with smaller font and light grey background
def display_metric_card(label, value):
    st.markdown(
        f"""
        <div style="background-color:#e6e6e6;padding:10px 15px;border-radius:5px;margin:10px 0;">
            <h5 style="margin:0;color:#333;font-size:16px;">{label}</h5>
            <p style="font-size:20px;margin:0;font-weight:bold;color:#007BFF;">{value}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Function to show detailed stages information
def show_detailed_stages_info():
    st.title("📊 Detailed Stages Information - Está TUDO chumbado :/")

    # Gather real data for each stage
    stages_data = {
        'Web Scraping': get_web_scraping_metrics(),
        'Data Parsing': get_data_parsing_metrics(),
        'Snowflake Loading': get_snowflake_loading_metrics(),
        'DBT Transformation': get_dbt_transformation_metrics(),
        'Final Data in Snowflake': get_final_snowflake_metrics(),
    }

    # Display each stage with its metrics in card format
    for stage, metrics in stages_data.items():
        st.markdown(f"## {stage}")
        with st.container():
            cols = st.columns(len(metrics))
            for col, (metric, value) in zip(cols, metrics.items()):
                with col:
                    display_metric_card(metric, value)
        st.markdown("---")  # Divider for visual separation

# Main function to control the navigation between pages
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["ETL Dashboard", "Detailed Stages Information"])

    if page == "ETL Dashboard":
        import show_etl_dashboard
        show_etl_dashboard()
    elif page == "Detailed Stages Information":
        show_detailed_stages_info()

# Run the app
if __name__ == "__main__":
    main()
