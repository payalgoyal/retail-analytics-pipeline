import pandas as pd
import sys
import os
from utils.generate_data import generate_data

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def extract_data():
    salesdf, customersdf, inventorydf = generate_data() 

    # Make bronze directory if it doesn't exist
    if not os.path.exists(os.path.join(project_root, 'data/bronze')):
        os.makedirs(os.path.join(project_root, 'data/bronze'))

    salesdf.to_csv(os.path.join(project_root, 'data/bronze/sales_bronze.csv'), index=False)
    customersdf.to_csv(os.path.join(project_root, 'data/bronze/customers_bronze.csv'), index=False)
    inventorydf.to_csv(os.path.join(project_root, 'data/bronze/inventory_bronze.csv'), index=False)
