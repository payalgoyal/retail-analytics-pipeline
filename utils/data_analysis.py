import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

if not os.path.exists(os.path.join(project_root, 'reports/plots')):
    os.makedirs(os.path.join(project_root, 'reports/plots'))
if not os.path.exists(os.path.join(project_root, 'reports/csv')):
    os.makedirs(os.path.join(project_root, 'reports/csv'))

# Database connection
user = "root"
host = "localhost"
password = quote_plus("MySqlDb@1")
database = "online_retail_data"

engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:3306/{database}")

def segment_customer(row):
    r, f, m = row['R_Score'], row['F_Score'], row['M_Score']

    if r >= 4 and f >= 4 and m >= 4:
        return 'Champions'
    elif r >= 4 and f >= 3:
        return 'Loyal Customers'
    elif r >= 3 and f >= 3:
        return 'Potential Loyalist'
    elif r <= 2 and f >= 3:
        return 'At Risk'
    elif r <= 2 and f <= 2 and m <= 2:
        return 'Hibernating'
    elif r == 3:
        return 'Needs Attention'
    else:
        return 'Others'

# Load gold sales table
df = pd.read_sql("SELECT * FROM sales_gold", engine)

# Analysis 1 (Top 10 selling products by Price)
top_products = df.groupby("Description")["TotalPrice"].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(12,6))
sns.barplot(x=top_products.values, y=top_products.index, palette="viridis")
plt.title("Top 10 Products by Total Sales")
plt.xlabel("Total Sales (£)")
plt.ylabel("Product Description")
plt.tight_layout()
plt.savefig(os.path.join(project_root,'reports/plots',"top_products_sales.png"))
plt.show()
plt.close()
print("Plot saved as top_products_sales.png")

# Analysis 2 (Monthly Revenue Trend)
monthly_revenue = df.groupby(['InvoiceYear', 'InvoiceMonth'])['TotalPrice'].sum().reset_index()
monthly_revenue['Month'] = monthly_revenue['InvoiceYear'].astype(str) + '-' + monthly_revenue['InvoiceMonth'].astype(str)

# Step 2: Sort by Month
monthly_revenue = monthly_revenue.sort_values('Month')

# Step 3: Select last 6 months
last_6_months = monthly_revenue.tail(6).reset_index(drop=True)

plt.figure(figsize=(12,5))
sns.lineplot(data=last_6_months, x='Month', y='TotalPrice', marker='o')
plt.title('Monthly Revenue Trend (Last 6 Months)')
plt.xlabel('Month')
plt.ylabel('Total Revenue (£)')
plt.tight_layout()
plt.savefig(os.path.join(project_root,'reports/plots',"monthly_revenue_trend.png"))
plt.show()
print("Plot saved as monthly_revenue_trend.png")
plt.close()

# Analysis 3 (Top 10 average order value by country)
top_countries = df.groupby("Country")["TotalPrice"].mean().sort_values(ascending=False).head(10)

plt.figure(figsize=(12,6))
sns.barplot(x=top_countries.index, y=top_countries.values, palette="viridis")
plt.title("Top 10 Countries by Average Order Value")
plt.xlabel("Country")
plt.ylabel("Average Order Value (£)")
plt.tight_layout()
plt.savefig(os.path.join(project_root,'reports/plots',"top_countries_average_order_value.png"))
plt.show()
print("Plot saved as top_countries_average_order_value.png")
plt.close()

# Analysis 4 (Top 5 products by sales in country Norway)
norway_sales = df[df["Country"] == "Norway"].groupby("Description")["TotalPrice"].sum().sort_values(ascending=False).head(5)

plt.figure(figsize=(12,6))
sns.barplot(x=norway_sales.index, y=norway_sales.values, palette="viridis")
plt.title("Top 5 Products by Sales in Norway")
plt.xlabel("Product Description")
plt.ylabel("Total Sales (£)")
plt.tight_layout()
plt.savefig(os.path.join(project_root,'reports/plots',"norway_sales_top_products.png"))
plt.show()
print("Plot saved as norway_sales_top_products.png")
plt.close()

# Analysis 5 (Customer Segmentation)
# Load customer summary table
customer_df = pd.read_sql("SELECT * FROM customers_gold", engine)
customer_df['segment'] = customer_df.apply(segment_customer, axis=1)

segment_counts = customer_df['segment'].value_counts().reset_index()
segment_counts.columns = ['Segment', 'Customer Count']

plt.figure(figsize=(10, 5))
sns.barplot(data=segment_counts, x='Segment', y='Customer Count', palette='Set2')
plt.title('Customer Segments based on RFM')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(project_root,'reports/plots',"customer_segments_rfm.png"))
plt.show()
print("Plot saved as customer_segments_rfm.png")
plt.close()

if __name__ == "__main__":
    # Save the top products data to a CSV file
    top_products.to_csv(os.path.join(project_root,'reports/csv',"top_products.csv"), header=True)
    print("Top products data saved as top_products.csv")

    monthly_revenue.to_csv(os.path.join(project_root,'reports/csv',"monthly_revenue.csv"), index=False)
    print("Monthly revenue data saved as monthly_revenue.csv")

    top_countries.to_csv(os.path.join(project_root,'reports/csv',"top_countries.csv"), header=True)
    print("Top countries data saved as top_countries.csv")

    # Save the Norway sales data to a CSV file
    norway_sales.to_csv(os.path.join(project_root,'reports/csv',"norway_sales.csv"), header=True)
    print("Norway sales data saved as norway_sales.csv")

    # Save the customer segmentation data to a CSV file
    segment_counts.to_csv(os.path.join(project_root,'reports/csv',"customer_segments.csv"), index=False)

    # Close Database connection
    engine.dispose()
    print("Database connection closed.")