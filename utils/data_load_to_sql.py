import mysql.connector
from urllib.parse import quote_plus
import pandas as pd
import os
import sys
from sqlalchemy import create_engine, inspect
import logging

sys.path.append('/opt/airflow/utils')
project_root = os.getenv("AIRFLOW_HOME", "/opt/airflow")
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
#project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# DB credentials

user = "airflow"
host = "mysql"
password = "airflow"
database = "retail_analytics_airflow"

engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:3306/{database}')
conn = engine.connect()

def load_to_sql():
    logging.info("Started loading...")
    #table name 
    sales_table = 'sales_gold'

    inspector = inspect(engine)
    table_exists = inspector.has_table(sales_table)

    df = pd.read_csv(os.path.join(project_root, 'data/gold/sales_enriched_gold.csv'))

    if not table_exists:
        df.to_sql(name=sales_table, con=conn, index=False, if_exists='replace')
        print(f"✅ Table '{sales_table}' created and data inserted.")
    else:
        df.to_sql(name=sales_table, con=conn, index=False, if_exists='append')
        print(f"✅ Table '{sales_table}' exists. Data appended.")
    
    # Load customers data
    customers_table = 'customers_gold'

    inspector = inspect(engine)
    table_exists = inspector.has_table(customers_table)

    df = pd.read_csv(os.path.join(project_root, 'data/gold/customer_summary_gold.csv'))
    
    if not table_exists:
        df.to_sql(name=customers_table, con=conn, index=False, if_exists='replace')
        print(f"✅ Table '{customers_table}' created and data inserted.")
    else:
        df.to_sql(name=customers_table, con=conn, index=False, if_exists='append')
        print(f"✅ Table '{customers_table}' exists. Data appended.")
   

    # Load inventory data
    inventory_table = 'inventory_gold'

    inspector = inspect(engine)
    table_exists = inspector.has_table(inventory_table)

    df = pd.read_csv(os.path.join(project_root, 'data/gold/inventory_gold.csv'))

    if not table_exists:
        df.to_sql(name=inventory_table, con=conn, index=False, if_exists='replace')
        print(f"✅ Table '{inventory_table}' created and data inserted.")
    else:
        df.to_sql(name=inventory_table, con=conn, index=False, if_exists='append')
        print(f"✅ Table '{inventory_table}' exists. Data appended.")
    
    conn.close()
   
if __name__ == "__main__":
    load_to_sql()
    print("Data loaded to SQL successfully.")   