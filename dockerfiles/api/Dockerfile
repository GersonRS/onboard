FROM python:3.9-slim

WORKDIR /usr/app

RUN pip install --upgrade pip
RUN pip install mlflow aiohttp

EXPOSE 8080

CMD python app.py