import streamlit as st
import pandas as pd  # Ensure pandas is imported
import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from get_data_from_snowflake_db import get_data_from_snowflake
from time import sleep, time

# Load environment variables
load_dotenv()

conn_params = {
    'user': os.getenv("SNOWFLAKE_USER"),
    'password': os.getenv("SNOWFLAKE_PASSWORD"),
    'account': os.getenv("SNOWFLAKE_ACCOUNT"),
    'database': os.getenv("SNOWFLAKE_DATABASE"),
    'warehouse': os.getenv("SNOWFLAKE_WAREHOUSE"),
    'schema': os.getenv("SNOWFLAKE_SCHEMA")
}

# Define the function to trigger and monitor the DBT job
def trigger_dbt_job():
    start_date = time()
    check_dbt = False
    DBT_CLOUD_API_TOKEN = os.getenv("DBT_CLOUD_API_TOKEN")
    ACCOUNT_ID = os.getenv("DBT_CLOUD_ACCOUNT_ID")
    PROJECT_ID = os.getenv("DBT_CLOUD_PROJECT_ID")
    JOB_ID = os.getenv("DBT_CLOUD_JOB_ID")

    headers = {
        "Authorization": f"Token {DBT_CLOUD_API_TOKEN}",
        "Content-Type": "application/json",
    }

    data = {"cause": "Triggered via Streamlit App"}

    trigger_job_url = (
        f"https://cloud.getdbt.com/api/v2/accounts/{ACCOUNT_ID}/jobs/{JOB_ID}/run/"
    )

    try:
        # Trigger the job
        response = requests.post(trigger_job_url, headers=headers, json=data)
        response.raise_for_status()  # Raises an error for HTTP codes 4xx/5xx

        run_data = response.json()["data"]
        run_id = run_data["id"]
        st.info(f"Job initiated successfully! Run ID: {run_id}")

        check_run_url = (
            f"https://cloud.getdbt.com/api/v2/accounts/{ACCOUNT_ID}/runs/{run_id}/"
        )

        run_status = "running"
        while run_status not in ["Success", "Error", "Cancelled"]:
            sleep(10)
            try:
                status_response = requests.get(check_run_url, headers=headers)
                status_response.raise_for_status()  # Raises an error for HTTP codes 4xx/5xx
                run_status = status_response.json()["data"]["status_humanized"]
                st.write(f"Current job status: {run_status}")
            except requests.RequestException as e:
                st.error(f"Error checking job status: {e}")
                run_status = "Error"  # Set to error to break the loop in case of repeated failures

        if run_status == "Success":
            st.success(f"Job completed with status: {run_status}")
            check_dbt = True
        else:
            st.error(f"Job completed with status: {run_status}")
    except requests.RequestException as e:
        st.error(f"Error starting the job: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
    end_date = time()
    execution_time = round(end_date - start_date, 2)
    return check_dbt, execution_time

# Define the function to show the ETL dashboard
def show_etl_dashboard():
    # Streamlit page configuration
    check_dbt = None
    etl_data_status_dbt = "Waiting"
    st.title("ETL Process Overview Dashboard")

    dbt_execution_time = 0
    st.subheader("Run DBT Jobs")

    # Trigger DBT job and monitor its status
    if st.button('Trigger DBT Job'):
        check_dbt, dbt_execution_time = trigger_dbt_job()

    check_snowflake, sf_update_at, sf_execution_time = get_data_from_snowflake(**conn_params)
    etl_data_status_sf = "Success" if check_snowflake else "Failed"
    etl_data_status_dbt = "Success" if check_dbt else "Failed"

    etl_data = {
        'Stage': ['Loading to Snowflake', 'DBT Transformation', 'Final Load to Snowflake'],
        'Status': [etl_data_status_sf, etl_data_status_dbt, etl_data_status_sf],
        'Last Run Time': [
            sf_update_at,
            datetime.now() - timedelta(hours=2),
            sf_update_at
        ],
        'Next Scheduled Run': [
            datetime.now() + timedelta(days=1),
            datetime.now() + timedelta(days=1),
            datetime.now() + timedelta(days=1)
        ],
        'Execution Duration (seconds)': [sf_execution_time, dbt_execution_time, sf_execution_time],
        'Error Alerts': ['Success', 'Success', 'Success']
    }

    # Convert the data to a DataFrame
    df = pd.DataFrame(etl_data)


    # Display the pipeline status with color indicators
    if check_dbt:
        st.subheader("Pipeline Status")
        for index, row in df.iterrows():
            status_color = "green" if row['Status'] == 'Success' else ("red" if row['Status'] == 'Failed' else "orange")
            st.markdown(f"<span style='color:{status_color}; font-weight:bold;'>{row['Stage']}: {row['Status']}</span>", unsafe_allow_html=True)

        # Display last run times
        st.subheader("Last Run Time")
        st.dataframe(df[['Stage', 'Last Run Time']])

        # Display next scheduled runs
        st.subheader("Next Scheduled Run")
        st.dataframe(df[['Stage', 'Next Scheduled Run']])

        # Display execution durations
        st.subheader("Execution Duration")
        st.dataframe(df[['Stage', 'Execution Duration (seconds)']])


# Run the ETL dashboard in the Streamlit app
if __name__ == "__main__":
    show_etl_dashboard()
