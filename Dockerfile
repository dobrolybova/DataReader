FROM python:3.10-alpine

WORKDIR /DataReader

COPY requirements.txt ./
COPY README.md ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./src ./src
