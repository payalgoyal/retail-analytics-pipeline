import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def data_transformation():
    sales_df = pd.read_csv(os.path.join(project_root, 'data/silver/sales_silver.csv'))

    # Create a new column for total price
    sales_df['TotalPrice'] = sales_df['Quantity'] * sales_df['UnitPrice']

    customers_df = pd.read_csv(os.path.join(project_root, 'data/silver/customers_silver.csv'))

    # Merge sales and customers data
    sales_cust_df = pd.merge(sales_df, customers_df, on='CustomerID', how='left')

    # Ensure InvoiceDate is in datetime format
    sales_cust_df['InvoiceDate'] = pd.to_datetime(sales_cust_df['InvoiceDate'], errors='coerce')
    sales_cust_df['InvoiceYear'] = pd.to_datetime(sales_cust_df['InvoiceDate']).dt.year
    sales_cust_df['InvoiceMonth'] = pd.to_datetime(sales_cust_df['InvoiceDate']).dt.to_period('M')
    sales_cust_df['InvoiceDay'] = pd.to_datetime(sales_cust_df['InvoiceDate']).dt.day
    sales_cust_df['InvoiceHour'] = pd.to_datetime(sales_cust_df['InvoiceDate']).dt.hour

    # Set reference date for recency calculation
    reference_date = sales_cust_df['InvoiceDate'].max() + pd.Timedelta(days=1)

    #Group by CustomerID and calculate total and avg sales
    cust_summary_df = (
        sales_cust_df
        .groupby('CustomerID')
        .agg(
            Total_Purchases=('InvoiceNo', 'nunique'),
            Recency=('InvoiceDate', lambda x: (reference_date - x.max()).days),
            Frequency=('InvoiceNo', 'nunique'),
            Monetary=('TotalPrice', 'sum'),
            Average_Spent=('TotalPrice', 'mean'),
        )
        .reset_index()
    )

    # Score R (lower is better, so reverse the rank)
    cust_summary_df['R_Score'] = pd.qcut(cust_summary_df['Recency'], 4, labels=[4, 3, 2, 1])

    # Score F (higher is better)
    cust_summary_df['F_Score'] = pd.qcut(cust_summary_df['Frequency'].rank(method='first'), 4, labels=[1, 2, 3, 4])

    # Score M (higher is better)
    cust_summary_df['M_Score'] = pd.qcut(cust_summary_df['Monetary'].rank(method='first'), 4, labels=[1, 2, 3, 4])

    cust_summary_df['RFM_Score'] = (
        cust_summary_df['R_Score'].astype(int).astype(str) +
        cust_summary_df['F_Score'].astype(int).astype(str) +
        cust_summary_df['M_Score'].astype(int).astype(str)
    )

    # Step 3: Segment as Loyal or Others
    cust_summary_df['Customer_Type'] = cust_summary_df['RFM_Score'].apply(
        lambda score: 'Loyal' if score >= '333' else 'Others'
    )

    cust_summary_df['Is_Returning'] = cust_summary_df['Total_Purchases'] > 1

    # Inventory Analysis
    inventory_df = pd.read_csv(os.path.join(project_root, 'data/silver/inventory_silver.csv'))

    # Merge LastUpdated into sales_df (to know the cutoff for each product)
    sales_with_update = pd.merge(
        sales_df,
        inventory_df[['StockCode', 'LastUpdated']],
        on='StockCode',
        how='left'
    )

    # 🔍 Step 1: Filter sales that occurred **after** inventory LastUpdated
    sales_after_update = sales_with_update[sales_with_update['InvoiceDate'] > sales_with_update['LastUpdated']]

    # 🔢 Step 2: Group to get total quantity sold after LastUpdated
    sold_quantity = (
        sales_after_update.groupby('StockCode')['Quantity']
        .sum()
        .reset_index()
        .rename(columns={'Quantity': 'Total_Sold'})
    )

    # 📦 Step 3: Subtract from Stock
    inventory_df = pd.merge(inventory_df, sold_quantity, on='StockCode', how='left')
    inventory_df['Total_Sold'] = inventory_df['Total_Sold'].fillna(0)
    inventory_df['New_Stock'] = inventory_df['Stock'] - inventory_df['Total_Sold']
    inventory_df['Stock'] = inventory_df['Stock'].clip(lower=0)

    # Make gold directory if it doesn't exist
    if not os.path.exists(os.path.join(project_root, 'data/gold')):
        os.makedirs(os.path.join(project_root, 'data/gold'))

    sales_cust_df.to_csv(os.path.join(project_root, 'data/gold/sales_enriched_gold.csv'), index=False)
    cust_summary_df.to_csv(os.path.join(project_root, 'data/gold/customer_summary_gold.csv'), index=False)
    inventory_df.to_csv(os.path.join(project_root, 'data/gold/inventory_gold.csv'), index=False)

if __name__ == "__main__":
    data_transformation()