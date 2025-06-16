FROM apache/airflow:2.8.1

USER root

RUN apt-get update && apt-get install -y openjdk-17-jdk default-libmysqlclient-dev gcc && apt-get clean

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

USER airflow

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt \
    --constraint https://raw.githubusercontent.com/apache/airflow/constraints-2.8.1/constraints-3.8.txt
