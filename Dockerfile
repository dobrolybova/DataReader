FROM python:latest

WORKDIR /DataReader

COPY requirements.txt ./
COPY README.md ./

run pip install --no-cache-dir -r requirements.txt

COPY ./src ./src
