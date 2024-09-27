import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import random

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

# Function to display Airflow pipeline status
def show_airflow_pipeline(df):
    st.subheader("🚀 Airflow Pipeline Status")

    # Display task statuses
    st.dataframe(df[['Task Name', 'Status', 'Start Time', 'End Time', 'Duration (min)']])

    # Visualize pipeline status
    fig, ax = plt.subplots(figsize=(10, 4))
    for index, row in df.iterrows():
        color = 'green' if row['Status'] == 'Success' else 'red' if row['Status'] == 'Failed' else 'orange'
        ax.barh(row['Task Name'], row['Duration (min)'], color=color, edgecolor='black')

    ax.set_xlabel("Duration (min)")
    ax.set_ylabel("Task Name")
    ax.set_title("Airflow Pipeline Task Durations")
    st.pyplot(fig)

# Function to show the main page
def show_airflow_pipeline_page():
    st.title("Airflow Pipeline Dashboard")

    # Button to run the pipeline
    if st.button("Run Pipeline"):
        # Generate new pipeline data when the button is clicked
        df = generate_airflow_pipeline_data()

        # Show the Airflow pipeline status
        show_airflow_pipeline(df)
    else:
        st.write("Click the 'Run Pipeline' button to execute the pipeline and see the results.")

if __name__ == "__main__":
    show_airflow_pipeline_page()
