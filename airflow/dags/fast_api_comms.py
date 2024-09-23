from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import requests

def test_communication():
    try:
        response = requests.get('http://app_fastapi:8000/health')
        if response.status_code == 200:
            print("Comunicação bem-sucedida com app_fastapi!")
        else:
            print(f"Falha na comunicação. Status Code: {response.status_code}")
            raise Exception("Falha na comunicação com app_fastapi.")
    except Exception as e:
        print(str(e))
        raise

default_args = {
    'start_date': datetime(2023, 1, 1),
}

with DAG(
    dag_id="fastapi_communication_dag",
    default_args=default_args,
    schedule_interval="@once",
    catchup=False,
) as dag:
    test_task = PythonOperator(
        task_id='fastapi_communication_task',
        python_callable=test_communication
)
