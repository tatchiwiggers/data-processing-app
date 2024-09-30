import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import random

# Apply custom CSS for enhanced styling
st.markdown("""
    <style>
        .main-header {
            font-size: 36px;
            font-weight: bold;
            color: #003366;
            text-align: center;
        }
        .sub-header {
            font-size: 24px;
            font-weight: bold;
            color: #0066cc;
            margin-top: 20px;
        }
        .info-box {
            background-color: #e7f3ff;
            border-left: 5px solid #0066cc;
            padding: 10px;
            border-radius: 5px;
            margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# Function to simulate Airflow pipeline data
def generate_airflow_pipeline_data():
    tasks = ["Extract", "Transform", "Load", "Validate"]
    status = ["Success", "Failed", "Running", "Queued"]
    start_time = datetime.now() - timedelta(days=1)

    pipeline_data = {
        "Task Name": tasks,
        "Status": [random.choice(status) for _ in tasks],
        "Start Time": [start_time + timedelta(minutes=10*i) for i in range(len(tasks))],
        "End Time": [start_time + timedelta(minutes=10*i + random.randint(5, 10)) for i in range(len(tasks))],
        "Duration (min)": [random.randint(5, 10) for _ in tasks]
    }

    return pd.DataFrame(pipeline_data)
st.write("-----------------------------------")
# Function to display Airflow pipeline status
st.markdown("<br>", unsafe_allow_html=True)

def show_airflow_pipeline():
    st.markdown("<div class='sub-header'>🚀 Airflow Pipeline Status</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)


    from streamlit.components.v1 import html
    from airflow.api.client.local_client import Client
    # Embed the Airflow UI using an iframe

    open_script= """
        <script type="text/javascript">
            window.open('http://localhost:8080', '_blank').focus();
        </script>
    """

    if st.button('Run Airflow Dag'):
        html(open_script)
        st.write("Airflow DAG is running...")



st.write("""
This dashboard allows you to simulate and visualize the status of an Airflow pipeline.
Click the button below to run the pipeline and see the results.
""")

st.markdown("<br>", unsafe_allow_html=True)

if __name__ == "__main__":
    show_airflow_pipeline()
