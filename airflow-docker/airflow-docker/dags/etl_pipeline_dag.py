from airflow import DAG
from airflow.operators.python import PythonOperator
import pandas as pd
import sys
import os
from datetime import datetime, timedelta

sys.path.append('/opt/airflow/utils')
project_root = os.getenv("AIRFLOW_HOME", "/opt/airflow")

#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from data_extract import extract_data
from data_cleaning import data_cleaning
from data_transformation import data_transformation
from generate_data import generate_data
from data_load_to_sql import load_to_sql
from data_analysis import analysis

default_args = {
    'owner' : 'airflow',
    'start_date' : datetime(2025,6,14),
    'retries': 3,
    'retry_delay': timedelta(minutes=1),   
}

dag = DAG(
    'retail_analytics_airflowDAG',
    default_args = default_args,
    schedule_interval = '@daily',
    catchup=False,
    doc_md = """
        ### Retail Analytics ETL Pipeline (Airflow Orchestration)
        This DAG performs daily ETL jobs for:
        - Extraction
        - Cleaning
        - Transformation
        - Loading to SQL
        """
)

extract_task = PythonOperator(
    task_id = 'extract',
    python_callable = extract_data,
    dag = dag,
    sla=timedelta(minutes=10)
)

clean_task = PythonOperator(
    task_id = 'clean',
    python_callable = data_cleaning,
    dag = dag,
)

transform_task = PythonOperator(
    task_id = 'transform',
    python_callable = data_transformation,
    dag = dag,
)

load_task = PythonOperator(
    task_id = 'load',
    python_callable = load_to_sql,
    dag = dag,
)

analysis_task = PythonOperator(
    task_id = 'analyse',
    python_callable = analysis,
    dag = dag,
)

extract_task >> clean_task >> transform_task >> load_task >> analysis_task
