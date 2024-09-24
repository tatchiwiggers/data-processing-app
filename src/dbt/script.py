import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

DBT_CLOUD_API_TOKEN = os.getenv("DBT_CLOUD_API_TOKEN")
ACCOUNT_ID = os.getenv("DBT_CLOUD_ACCOUNT_ID")
PROJECT_ID = os.getenv("DBT_CLOUD_PROJECT_ID")
JOB_ID = os.getenv("DBT_CLOUD_JOB_ID")

headers = {
    "Authorization": f"Token {DBT_CLOUD_API_TOKEN}",
    "Content-Type": "application/json",
}

data = {"cause": "Triggered via API"}

trigger_job_url = (
    f"https://cloud.getdbt.com/api/v2/accounts/{ACCOUNT_ID}/jobs/{JOB_ID}/run/"
)

response = requests.post(trigger_job_url, headers=headers, json=data)

if response.status_code == 200:
    run_data = response.json()["data"]
    run_id = run_data["id"]
    print(f"Job iniciada com sucesso! Run ID: {run_id}")

    check_run_url = (
        f"https://cloud.getdbt.com/api/v2/accounts/{ACCOUNT_ID}/runs/{run_id}/"
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
