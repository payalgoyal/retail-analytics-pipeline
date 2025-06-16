#!/bin/bash

airflow users create \
    --username airflow \
    --firstname Air \
    --lastname Flow \
    --role Admin \
    --email airflow@example.com \
    --password airflow