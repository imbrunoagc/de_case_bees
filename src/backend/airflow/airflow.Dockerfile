FROM apache/airflow:slim-latest-python3.12

COPY requirements.txt .
RUN pip install -r requirements.txt