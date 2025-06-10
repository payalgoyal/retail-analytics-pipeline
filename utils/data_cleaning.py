import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def clean_salesdf():
    # Load the data
    salesdf = pd.read_csv(os.path.join(project_root, 'data/bronze/sales_bronze.csv'))

    # Drop rows with missing values
    salesdf.dropna(subset=['CustomerID', 'StockCode','Quantity','UnitPrice'], inplace=True)
    salesdf['CustomerID'] = salesdf['CustomerID'].astype(int)
    
    #Remove Quantity less than 1
    salesdf = salesdf[salesdf['Quantity'] >= 1]

    # Remove rows with negative UnitPrice
    salesdf = salesdf[salesdf['UnitPrice'] >= 0]

    # Convert InvoiceDate to datetime
    salesdf['InvoiceDate'] = pd.to_datetime(salesdf['InvoiceDate'], errors='coerce')
    salesdf = salesdf[salesdf['InvoiceDate'] <= pd.Timestamp.now()]

    # Slice the first 5 characters of StockCode
    salesdf['StockCode'] = salesdf['StockCode'].astype(str).str.slice(0, 5)

    # Make silver directory if it doesn't exist
    if not os.path.exists(os.path.join(project_root, 'data/silver')):
        os.makedirs(os.path.join(project_root, 'data/silver'))

    # Save the cleaned data
    salesdf.to_csv(os.path.join(project_root, 'data/silver/sales_silver.csv'), index=False)

def clean_customersdf():
    # Load the data
    customersdf = pd.read_csv(os.path.join(project_root, 'data/bronze/customers_bronze.csv'))

    # Remove null CustomerID
    customersdf.dropna(subset=['CustomerID'], inplace=True)

    # Remove duplicate CustomerID
    customersdf.drop_duplicates(subset=['CustomerID'], inplace=True)

    #Strip leading and trailing spaces from Name, Email, Phone, Address
    customersdf['Name'] = customersdf['Name'].str.strip()
    customersdf['Email'] = customersdf['Email'].str.strip()
    customersdf['Phone'] = customersdf['Phone'].str.strip()
    customersdf['Address'] = customersdf['Address'].str.strip()

    #check valid email format
    valid_email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    customersdf['Email'] = customersdf['Email'].where(customersdf['Email'].str.match(valid_email_pattern, na=False), 'N/A')

    #Clean Phone numbers based on uk format 20 7123 4567 
    #phone numbers should be 11 digits long, and should be formatted as 20 - 7123 - 4567
    customersdf['Phone'] = customersdf['Phone'].str.replace(r'\D', '', regex=True)  # Remove non-digit characters

    customersdf['Phone'] = customersdf['Phone'].where(customersdf['Phone'].str.len() == 10, 'N/A')  # Keep only valid phone numbers

    # Format valid phone numbers
    customersdf.loc[customersdf['Phone'] != 'N/A', 'Phone'] = customersdf['Phone'].str.replace(r'(\d{2})(\d{4})(\d{4})', r'\1-\2-\3', regex=True)

    # Check valid signup date format
    customersdf['SignupDate'] = pd.to_datetime(customersdf['SignupDate'], errors='coerce')
    customersdf['SignupDate'] = customersdf['SignupDate'].where(customersdf['SignupDate'] <= pd.Timestamp.now(), pd.NaT)
    customersdf['SignupDate'] = customersdf['SignupDate'].fillna('N/A')

    #Save the cleaned data
    customersdf.to_csv(os.path.join(project_root, 'data/silver/customers_silver.csv'), index=False)   

def clean_inventorydf():
    
    inventorydf = pd.read_csv(os.path.join(project_root, 'data/bronze/inventory_bronze.csv')) 
    #Remove negative Stock values
    inventorydf = inventorydf[inventorydf['Stock'] >= 0]

    #Trim whitespace from StockCode and Description
    inventorydf['StockCode'] = inventorydf['StockCode'].astype(str).str.strip()
    
    # Remove duplicate StockCode
    inventorydf.drop_duplicates(subset=['StockCode'], inplace=True)

    # Remove rows with missing StockCode or Description
    inventorydf.dropna(subset=['StockCode'], inplace=True)

    # Remove updated dates that are in the future
    inventorydf['LastUpdated'] = pd.to_datetime(inventorydf['LastUpdated'], errors='coerce')
    inventorydf = inventorydf[inventorydf['LastUpdated'] <= pd.Timestamp.now()]

    #save the clecleraned data
    inventorydf.to_csv(os.path.join(project_root, 'data/silver/inventory_silver.csv'), index=False)

def data_cleaning():

    clean_salesdf()
    clean_customersdf()
    clean_inventorydf()

if __name__ == "__main__":
    data_cleaning()