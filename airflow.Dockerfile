FROM apache/airflow:2.10.0-python3.12

ENV PYTHONPATH="${PYTHONPATH}:/opt/airflow"

# Copia os requirements para dentro do container
COPY requirements.txt .
RUN pip install -r requirements.txt