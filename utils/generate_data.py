import pandas as pd
import sys
import os
from faker import Faker

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

faker = Faker()

def generate_data():
    sales_df = pd.read_excel(os.path.join(project_root, 'data/loaded/loaded_sales_data.xlsx'), sheet_name='Online Retail')
    sales_df['CustomerID'] = sales_df['CustomerID'].astype('Int64')

    # Generate customers data and store in customers.csv file
    customers = []
    customer_ids = sales_df['CustomerID'].unique()

    for customer_id in customer_ids:
        if pd.isna(customer_id):
            continue
        customers.append({
            'CustomerID': int(customer_id),
            'Name': faker.name(),
            'Email': faker.email(),
            'Phone': faker.phone_number(),
            'Address': faker.address(),
            'SignupDate': faker.date_between(start_date='-2y', end_date='today')
        })

    customers_df = pd.DataFrame(customers)
    
    #Generate inventory data and store in inventory.csv file
    inventory = []
    stock_codes = sales_df['StockCode'].unique()
    for stock_code in stock_codes:
        inventory.append({
            'StockCode': str(stock_code)[:5],  # Ensure StockCode is a string of max 5 characters
            'Stock': faker.random_int(min=100, max=20000),
            'LastUpdated': faker.date_between(start_date='-30d', end_date='today')
        })

    inventory_df = pd.DataFrame(inventory)

    return sales_df, customers_df, inventory_df

if __name__ == "__main__":
    generate_data()
