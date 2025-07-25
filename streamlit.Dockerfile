FROM python:3.12.2

WORKDIR /frontend

COPY requirements-frontend.txt /frontend/requirements-frontend.txt

RUN pip install --no-cache-dir --upgrade -r requirements-frontend.txt

COPY ./src/frontend /frontend

ENTRYPOINT ["streamlit", "run", "app.py"]