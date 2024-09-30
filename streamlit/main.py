import streamlit as st
from time import time
from datetime import datetime, timedelta

# Apply custom CSS for enhanced styling
st.markdown("""
    <style>
        .sidebar .sidebar-content {
            background-color: #f7f9fc;
        }
        .sidebar .sidebar-title {
            font-size: 24px;
            font-weight: bold;
            color: #003366;
        }
        .sidebar .sidebar-item {
            font-size: 18px;
            color: #333;
        }
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
        }
        .info-box-dark {
            background-color: #333333;
            color: #ffffff;
            border-left: 5px solid #0066cc;
            padding: 10px;
            border-radius: 5px;
        }
    </style>
""", unsafe_allow_html=True)

# Main app navigation
st.sidebar.title("Navigation", "sidebar-title")
page = st.sidebar.selectbox("Go to", ["Home", "Airflow Pipeline Dashboard", "ETL Overview Dashboard", "Historical Data", "Customizable Views"], format_func=lambda x: f"📄 {x}")

if page == "Home":
    # Home page content
    st.markdown("<div class='main-header'>🌟 Data Processing App 🌟</div>", unsafe_allow_html=True)
    st.write("""<hr style='border: 1px solid #e0e0e0;' />""", unsafe_allow_html=True)

    st.markdown("<div class='sub-header'>🔍 Overview</div>", unsafe_allow_html=True)
    st.write("""
        Welcome to our data processing app! This application provides a comprehensive overview of our ETL (Extract, Transform, Load) process,
        leveraging cutting-edge technologies like CI/CD, Kubernetes, DBT, Airflow, and Snowflake to deliver a robust, scalable, and efficient data pipeline.
    """)

    st.write("-----------------------------------")

    st.markdown("<div class='sub-header'>🛠️ Technologies Used</div>", unsafe_allow_html=True)
    st.markdown("""
        Our ETL pipeline integrates several advanced technologies to ensure efficiency, reliability, and scalability:
        - **CI/CD (Continuous Integration/Continuous Deployment)**: Automates the testing and deployment of the ETL pipeline, ensuring seamless integration and deployment.
        - **Kubernetes**: Orchestrates our containerized services, ensuring high availability and scalability.
        - **DBT (Data Build Tool)**: Transforms raw data into analytics-ready tables within the data warehouse.
        - **Airflow**: Manages and schedules ETL workflows, monitoring the process and alerting on failures.
        - **Snowflake**: A cloud-based data warehouse used to store both raw and transformed data.
    """, unsafe_allow_html=True)

    st.write("-----------------------------------")

    st.markdown("<div class='sub-header'>🔄 ETL Process Flow</div>", unsafe_allow_html=True)
    st.write("""
        The ETL process in this application is designed to efficiently process and transform data through the following stages:
        1. **Web Scraping**: Collects raw data from online sources.
        2. **Data Parsing**: Cleans and prepares the data for loading.
        3. **Loading to Snowflake**: Stores cleaned data in Snowflake.
        4. **DBT Transformation**: Applies transformation logic using DBT within Snowflake.
        5. **Orchestration with Airflow**: Manages the workflow and schedules tasks.
        6. **Deployment and Monitoring with CI/CD and Kubernetes**: Ensures the pipeline is always up-to-date and running efficiently.
    """)


    st.markdown("""
    ![](https://mermaid.ink/img/pako:eNqNVE1vm0AQ_SsjDj3FrcA3DpVsMEqUVorkqJG65DCGwUZedtHuosiN8t87gCMvMZHCAbEz7828-Vheg0KXFMRBJfVLcUDj4DHNFfBju93eYHuAFB1CoqWkwtVajd7-WYXiiXawLRhWq338DoKyZ1RGN7DVnSkIwmePFX2VFfms5VdZS58VwmLxE9ZiqOEBjWXuRMvo9_P4FlJlruba8WB0QbaPdqFOs7BCSagAVQnW8RtNWf-jQa-nYD2kS8QvjSWzwGnYKv1SSTxSDFunDUHLEan0mZ6uZAiQjrkfDSpbadNgP6nnee1T0EVKGopV28oTuAnAemrTSPxBWbMSuqCm0sZIo6jIZw6mjchqhRL6cmdrRfaeXF3YhSEsT58UvRmCZeJJm2O_ufCbeXtqSLnromdAF11ZKLbFgcpOckVoj361WSS4V8Vx3DFZK2K671-KlSS-MlpBhbXsDE3oYxeysfJs-flKJXc_khS-wX23I6PIkYU75YidHy8cLL5zrNtQDJQYVp3TTT-NklqpT-cG-Os94qcL_tG2vjYl16Y0nLHNZNhcm7IZajZDzWbE3b5zI3HpT3weJjfNFsiz49YP19_6yxLcBA3xGtcl_-Fee0ceuANvQB7E_MlX8pgHuXpjHHIjtydVBLEzHd0ERnf7QxBXKC2furZf-bRGHknzDmlR_dX6fHz7D-rxjL4?type=png)
    """, unsafe_allow_html=True)

    st.write("-----------------------------------")

    st.markdown("<div class='sub-header'>📄 How to Use This App</div>", unsafe_allow_html=True)
    st.write("""
        Use the sidebar to navigate between different sections of the app:
        - **Home**: Overview and navigation guide.
        - **ETL Overview Dashboard**: Detailed status and metrics of the ETL process.
    """)

    st.write("-----------------------------------")

    st.markdown("<div class='sub-header'>📊 Current Status Summary</div>", unsafe_allow_html=True)
    etl_run = datetime.now() - timedelta(hours=5)

    # Add 1 day to etl_run
    next_day_run = etl_run + timedelta(days=1)

    # Format both times to display them
    etl_run_str = etl_run.strftime("%Y-%m-%d %H:%M:%S")
    next_day_run_str = next_day_run.strftime("%Y-%m-%d %H:%M:%S")

    # Display the formatted times in your markdown
    st.markdown(f"""
        <div class="info-box-dark">
            <strong>Last ETL Run:</strong> {etl_run_str} <br>
            <strong>Current Status:</strong> Success <br>
            <strong>Next Scheduled Run:</strong> {next_day_run_str}
        </div>
    """, unsafe_allow_html=True)

    st.markdown("----")
    st.write("For more details, visit the **ETL Overview Dashboard** using the sidebar.")

elif page == "Airflow Pipeline Dashboard":
    import airflow_pipeline
    airflow_pipeline.show_airflow_pipeline()

elif page == "ETL Overview Dashboard":
    import show_etl_dashboard
    show_etl_dashboard.show_etl_dashboard()

elif page == "Historical Data":
    import generate_historical_data
    generate_historical_data.show_historical_data()

elif page == "Customizable Views":
    import get_etl_logs
    get_etl_logs.show_customizable_views_page()
