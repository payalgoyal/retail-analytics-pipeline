import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.data_extract import extract_data
from utils.data_cleaning import data_cleaning
from utils.data_transformation import data_transformation
from utils.generate_data import generate_data
from utils.data_load_to_sql import load_to_sql

def etl_pipeline():
    # ETL Pipeline
    # Step 1: Extract data
    print("Starting data extraction...")
    extract_data()
    print("Data extraction completed.")

    # Step 2: Clean data
    print("Starting data cleaning...")
    data_cleaning()
    print("Data cleaning completed.")

    # Step 3: Transform data
    print("Starting data transformation...")
    data_transformation()
    print("Data transformation completed.") 

    # Step 4: Load data to SQL
    print("Starting data loading to SQL...")
    load_to_sql()
    print("Data loading to SQL completed.")

if __name__ == "__main__":
    etl_pipeline()
    print("ETL pipeline completed successfully.")   
