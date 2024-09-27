import streamlit as st


# Main app navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Go to", ["Home", "Airflow Pipeline Dashboard", "ETL Overview Dashboard", "Detailed Stages Information", "Historical Data", "Customizable Views"])

if page == "Home":
    # Home page content
    st.title("🌟 Data Processing App 🌟")
    st.write("""---------------------------------""")
    # Add a banner image or logo if desired
    st.image("https://your-logo-url.com/logo.png", use_column_width=True)

    st.subheader("🔍 Overview")
    st.write("""
        Welcome to our data processing app! This application provides a comprehensive overview of our ETL (Extract, Transform, Load) process,
        leveraging cutting-edge technologies like CI/CD, Kubernetes, DBT, Airflow, and Snowflake to deliver a robust, scalable, and efficient data pipeline.
    """)

    st.subheader("🛠️ Technologies Used")
    st.markdown("""
        Our ETL pipeline integrates several advanced technologies to ensure efficiency, reliability, and scalability:
        - **CI/CD (Continuous Integration/Continuous Deployment)**: Automates the testing and deployment
          of the ETL pipeline, ensuring seamless integration and deployment.
        - **Kubernetes**: Orchestrates our containerized services, ensuring high availability and scalability.
        - **DBT (Data Build Tool)**: Transforms raw data into analytics-ready tables within the data warehouse.
        - **Airflow**: Manages and schedules ETL workflows, monitoring the process and alerting on failures.
        - **Snowflake**: A cloud-based data warehouse used to store both raw and transformed data.
    """, unsafe_allow_html=True)

    st.subheader("🔄 ETL Process Flow")
    st.write("""
        The ETL process in this application is designed to efficiently process and transform data through the following stages:
        1. **Web Scraping**: Collects raw data from online sources.
        2. **Data Parsing**: Cleans and prepares the data for loading.
        3. **Loading to Snowflake**: Stores cleaned data in Snowflake.
        4. **DBT Transformation**: Applies transformation logic using DBT within Snowflake.
        5. **Orchestration with Airflow**: Manages the workflow and schedules tasks.
        6. **Deployment and Monitoring with CI/CD and Kubernetes**: Ensures the pipeline is always up-to-date and running efficiently.
    """)

    # Add a flowchart or diagram if available
    st.markdown("[![](https://mermaid.ink/img/pako:eNqNVE1vm0AQ_SsjDj3FrcA3DpVsMEqUVorkqJG65DCGwUZedtHuosiN8t87gCMvMZHCAbEz7828-Vheg0KXFMRBJfVLcUDj4DHNFfBju93eYHuAFB1CoqWkwtVajd7-WYXiiXawLRhWq338DoKyZ1RGN7DVnSkIwmePFX2VFfms5VdZS58VwmLxE9ZiqOEBjWXuRMvo9_P4FlJlruba8WB0QbaPdqFOs7BCSagAVQnW8RtNWf-jQa-nYD2kS8QvjSWzwGnYKv1SSTxSDFunDUHLEan0mZ6uZAiQjrkfDSpbadNgP6nnee1T0EVKGopV28oTuAnAemrTSPxBWbMSuqCm0sZIo6jIZw6mjchqhRL6cmdrRfaeXF3YhSEsT58UvRmCZeJJm2O_ufCbeXtqSLnromdAF11ZKLbFgcpOckVoj361WSS4V8Vx3DFZK2K671-KlSS-MlpBhbXsDE3oYxeysfJs-flKJXc_khS-wX23I6PIkYU75YidHy8cLL5zrNtQDJQYVp3TTT-NklqpT-cG-Os94qcL_tG2vjYl16Y0nLHNZNhcm7IZajZDzWbE3b5zI3HpT3weJjfNFsiz49YP19_6yxLcBA3xGtcl_-Fee0ceuANvQB7E_MlX8pgHuXpjHHIjtydVBLEzHd0ERnf7QxBXKC2furZf-bRGHknzDmlR_dX6fHz7D-rxjL4?type=png)](https://mermaid.live/edit#pako:eNqNVE1vm0AQ_SsjDj3FrcA3DpVsMEqUVorkqJG65DCGwUZedtHuosiN8t87gCMvMZHCAbEz7828-Vheg0KXFMRBJfVLcUDj4DHNFfBju93eYHuAFB1CoqWkwtVajd7-WYXiiXawLRhWq338DoKyZ1RGN7DVnSkIwmePFX2VFfms5VdZS58VwmLxE9ZiqOEBjWXuRMvo9_P4FlJlruba8WB0QbaPdqFOs7BCSagAVQnW8RtNWf-jQa-nYD2kS8QvjSWzwGnYKv1SSTxSDFunDUHLEan0mZ6uZAiQjrkfDSpbadNgP6nnee1T0EVKGopV28oTuAnAemrTSPxBWbMSuqCm0sZIo6jIZw6mjchqhRL6cmdrRfaeXF3YhSEsT58UvRmCZeJJm2O_ufCbeXtqSLnromdAF11ZKLbFgcpOckVoj361WSS4V8Vx3DFZK2K671-KlSS-MlpBhbXsDE3oYxeysfJs-flKJXc_khS-wX23I6PIkYU75YidHy8cLL5zrNtQDJQYVp3TTT-NklqpT-cG-Os94qcL_tG2vjYl16Y0nLHNZNhcm7IZajZDzWbE3b5zI3HpT3weJjfNFsiz49YP19_6yxLcBA3xGtcl_-Fee0ceuANvQB7E_MlX8pgHuXpjHHIjtydVBLEzHd0ERnf7QxBXKC2furZf-bRGHknzDmlR_dX6fHz7D-rxjL4)")

    st.subheader("📄 How to Use This App")
    st.write("""
        Use the sidebar to navigate between different sections of the app:
        - **Home**: Overview and navigation guide.
        - **ETL Overview Dashboard**: Detailed status and metrics of the ETL process.
    """)

    st.subheader("📊 Current Status Summary")
    st.info("""
        - **Last ETL Run**: 3 hours ago
        - **Current Status**: 1 stage failed
        - **Next Scheduled Run**: In 1 hour
    """)

    st.markdown("----")
    st.write("For more details, visit the **ETL Overview Dashboard** using the sidebar.")

elif page == "Airflow Pipeline Dashboard":
    import airflow_pipeline
    airflow_pipeline.show_airflow_pipeline_page()

elif page == "ETL Overview Dashboard":
    import show_etl_dashboard
    show_etl_dashboard.show_etl_dashboard()

elif page == "Detailed Stages Information":
    import show_detailed_stages_info
    show_detailed_stages_info.show_detailed_stages_info()

elif page == "Historical Data":
    import generate_historical_data
    generate_historical_data.show_historical_data()

elif page == "Customizable Views":
    import get_etl_logs
    get_etl_logs.show_customizable_views_page()
