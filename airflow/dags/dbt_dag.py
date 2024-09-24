from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable
import requests
import time
from datetime import timedelta

# Recupera as variáveis de ambiente usando Airflow Variables
DBT_CLOUD_API_TOKEN = Variable.get("DBT_CLOUD_API_TOKEN")
ACCOUNT_ID = Variable.get("ACCOUNT_ID")
PROJECT_ID = Variable.get("PROJECT_ID")
JOB_ID = Variable.get("JOB_ID")


default_args = {
    'owner': 'airflow',
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

def trigger_dbt_cloud_job(dbt_cloud_api_token, account_id, project_id, job_id, **context):
    headers = {
        "Authorization": f"Token {dbt_cloud_api_token}",
        "Content-Type": "application/json",
    }

    data = {"cause": "Triggered via API"}

    trigger_job_url = (
        f"https://cloud.getdbt.com/api/v2/accounts/{account_id}/jobs/{job_id}/run/"
    )
    response = requests.post(trigger_job_url, headers=headers, json=data)

    if response.status_code == 200:
        run_data = response.json()["data"]
        run_id = run_data["id"]
        print(f"Job iniciada com sucesso! Run ID: {run_id}")
        check_run_url = (
        f"https://cloud.getdbt.com/api/v2/accounts/{account_id}/runs/{run_id}/"
        )
        run_status = "running"
        while run_status not in ["Success", "Error", "Cancelled"]:
            time.sleep(10)
            status_response = requests.get(check_run_url, headers=headers)
            run_status = status_response.json()["data"]["status_humanized"]
            print(f"Status atual da Job: {run_status}")

        print(f"Job finalizada com status: {run_status}")
    else:
        print(f"Erro ao iniciar a Job: {response.status_code}, {response.text}")

with DAG(
    dag_id='dbt_cloud_job_trigger',
    default_args=default_args,
    description='DAG para disparar e monitorar um job no DBT Cloud',
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
) as dag:

    trigger_dbt_cloud_job_task = PythonOperator(
        task_id='trigger_dbt_cloud_job',
        python_callable=trigger_dbt_cloud_job,
        op_kwargs={
            'dbt_cloud_api_token': DBT_CLOUD_API_TOKEN,
            'account_id': ACCOUNT_ID,
            'project_id': PROJECT_ID,
            'job_id': JOB_ID,
        },
    )

    trigger_dbt_cloud_job_task
