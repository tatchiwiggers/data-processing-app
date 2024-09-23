FROM apache/airflow:2.10.2

USER root

RUN apt-get update && apt-get install -y \
    curl

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

COPY ./pyproject.toml ./poetry.lock ./

RUN poetry install --no-root

COPY src/webscraping_ml /opt/airflow/webscraping_ml

COPY .env /opt/airflow/webscraping_ml

USER airflow
