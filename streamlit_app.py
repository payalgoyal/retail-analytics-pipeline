import streamlit as st
import pandas as pd
from datetime import datetime
import altair as alt
import os
import plotly.express as px

@st.cache_data
def load_csv(path):
    return pd.read_csv(path)

def rfm_segment(row):
    if row['R_Score'] >= 4 and row['F_Score'] >= 4 and row['M_Score'] >= 4:
        return 'Champions'
    elif row['F_Score'] >= 4 and row['M_Score'] >= 3:
        return 'Loyal Customers'
    elif row['R_Score'] >= 3 and row['F_Score'] >= 3:
        return 'Potential Loyalists'
    elif row['R_Score'] >= 4:
        return 'Recent Customers'
    elif row['F_Score'] >= 4:
        return 'Frequent Buyers'
    elif row['M_Score'] >= 4:
        return 'Big Spenders'
    else:
        return 'Others'
                    
def main():
    st.title("Retail Analysis Dashboard")
    st.markdown("***This dashboard provides insights into retail sales data, including top products, monthly revenue, and customer segmentation.***")

    df = load_csv(os.path.join("data/gold", "sales_enriched_gold.csv"))

    # Date filter from sidebar
    min_date = pd.to_datetime(df['InvoiceDate'].min())
    max_date = pd.to_datetime(df['InvoiceDate'].max())

    # Get first day of the current (latest) month
    current_month_start = pd.to_datetime(f"{max_date.year}-{max_date.month}-01")

    # Get previous month start and end
    if max_date.month == 1:
        prev_month = 12
        prev_year = max_date.year - 1
    else:
        prev_month = max_date.month - 1
        prev_year = max_date.year

    prev_month_start = pd.to_datetime(f"{prev_year}-{prev_month}-01")
    prev_month_end = current_month_start - pd.Timedelta(days=1)

    # Use these for date input
    date_range = st.sidebar.date_input(
        "Select Date Range",
        [prev_month_start, prev_month_end],
        min_value=df['InvoiceDate'].min(),
        max_value=df['InvoiceDate'].max()
    )

    # Filter dataset
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    filtered_df = df[(df['InvoiceDate'] >= pd.to_datetime(date_range[0])) & (df['InvoiceDate'] <= pd.to_datetime(date_range[1]))]

    st.subheader("Key Metrics")
    st.markdown(f"**Data Range:** {date_range[0]} to {date_range[1]}")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Revenue", filtered_df["TotalPrice"].sum().round(2))
    col2.metric("Total Orders", filtered_df["InvoiceNo"].nunique())
    col3.metric("Total Customers", filtered_df["CustomerID"].nunique())    
    
    available_files = [f for f in os.listdir("data/gold") if f.endswith(".csv")]
    selected_file = st.sidebar.selectbox("Select Gold Layer Dataset", available_files)
    
    if selected_file.split('.')[0] == "customer_summary_gold":
        st.write(f"Get analysis for {selected_file.split('.')[0]}")
        if st.button("Get Data for Customer Summary"):
            df = load_csv(os.path.join("data/gold", selected_file))
            st.dataframe(df)

    elif selected_file.split('.')[0] == "sales_enriched_gold":
        st.write(f"Get analysis for {selected_file.split('.')[0]}")
        if st.button("Get Data for Sales Enriched"):
            df = load_csv(os.path.join("data/gold", selected_file))
            st.dataframe(df)

    elif selected_file.split('.')[0] == "inventory_gold":
        st.write(f"Get analysis for {selected_file.split('.')[0]}")
        if st.button("Get Data for Inventory"):
            df = load_csv(os.path.join("data/gold", selected_file))
            st.dataframe(df)

    country = st.sidebar.selectbox("Select Country", df['Country'].unique())
    country_df = df[df['Country'] == country] 

    # Get total revenue for selected country
    if country:
        total_revenue = df[df['Country'] == country]["TotalPrice"].sum().round(2)
        st.subheader(f"Analysis for {country}")

        with st.expander("Get Total Revenue"):
            st.markdown(f"**Total Revenue in {country} from {date_range[0]} to {date_range[1]} :  {total_revenue}**")
            if st.button("**Get Total Revenue Chart**"):            
                # Create a 'YearMonth' column for grouping
                country_df['YearMonth'] = country_df['InvoiceDate'].dt.to_period('M').astype(str) 
                monthly_revenue = country_df.groupby('YearMonth')['TotalPrice'].sum()
                st.line_chart(monthly_revenue,color="#328212")
        
        with st.expander("Top Selling Products"):
            st.markdown(f"**Top Selling Products in {country} from {date_range[0]} to {date_range[1]}**")
            top_products = (
                    country_df.groupby('Description')['TotalPrice']
                    .sum()
                    .round(2)
                    .sort_values(ascending=False)
                    .head(10)
                    .reset_index()
                )
            st.write(top_products.iloc[0])
            if st.button("Get Top Selling Products Chart"):
                # Bar chart for top selling products in different countries
                bar_chart = alt.Chart(top_products).mark_bar().encode(
                    x=alt.X('TotalPrice:Q', title='Total Sales'),
                    y=alt.Y('Description:N', sort='-x', title='Product Description'),
                    tooltip=['Description', 'TotalPrice']
                ).properties(
                    width=600,
                    height=400,
                    title='Top 10 Products by Sales'
                )

                # Show in Streamlit
                st.altair_chart(bar_chart, use_container_width=True)

        with st.expander("Customer Segmentation"):
            st.markdown(f"**Customer Segmentation in {country} from {date_range[0]} to {date_range[1]}**")
            if st.button("Get Customer Segmentation chart"):
                cust_df = load_csv(os.path.join("data/gold", "customer_summary_gold.csv"))
                cust_sales_df = pd.merge(df, cust_df, on='CustomerID', how='inner', suffixes=('', '_cust'))
                #pie chart for customer segmentation 
                
                cust_sales_df['Segment'] = cust_sales_df.apply(rfm_segment, axis=1)
                country_filtered = cust_sales_df[cust_sales_df['Country'] == country]
                segment_counts = country_filtered['Segment'].value_counts().reset_index()
                segment_counts.columns = ['Segment', 'CustomerCount']

                fig = px.pie(segment_counts,
                            values='CustomerCount',
                            names='Segment',
                            title=f'Customer Segmentation in {country}',
                            color_discrete_sequence=px.colors.qualitative.Set2)

                st.plotly_chart(fig, use_container_width=True)


        with st.expander("Top Customers"):
            st.markdown(f"**Top Customer in {country} from {date_range[0]} to {date_range[1]}**")
            top_customer = country_df.groupby("CustomerID")["TotalPrice"].sum().sort_values(ascending=False).reset_index(name="Customer_Revenue").head(10)
            #write 1st row of the df
            st.write(top_customer.iloc[0])
            if st.button("Get Top 10 Customers Table"):
                st.write(top_customer)

    with st.expander("Customer Country Distribution"):
        st.markdown(f"**Customer Country Distribution from {date_range[0]} to {date_range[1]}**")
        customer_country_df = df.groupby("Country")["CustomerID"].nunique().sort_values(ascending=False).reset_index(name="Customer_Count")
        st.write(customer_country_df.iloc[0])
        if st.button("Get Customer Country Distribution"): 
            st.write(customer_country_df)

    with st.expander("Summary"):
        st.markdown(f"""
        - Showing insights for **{country}** from **{date_range[0]}** to **{date_range[1]}**
        - Based on **{len(filtered_df)}** transactions from **{filtered_df['CustomerID'].nunique()}** customers
        """)


if __name__ == "__main__":
    main()