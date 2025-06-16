# 🛍️ Retail Analytics ETL Pipeline (Airflow Orchestration + MySQL + Streamlit)

[![Made with Streamlit](https://img.shields.io/badge/Made%20with-Streamlit-blue)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.10-blue)]

## Summary
This project implements a full batch ETL pipeline for Retail Analytics using Apache Airflow orchestration. The pipeline extracts, cleans, transforms, and loads sales data into MySQL, followed by business dashboard development using Streamlit.

It follows a Medallion Architecture (Bronze → Silver → Gold) and includes customer segmentation, revenue analysis, and business KPIs.

---

## 🔧 Tech Stack

- Python, Pandas, MySQL, Airflow, SQLAlchemy, Seaborn, Streamlit, Faker
- Apache Airflow (Orchestration: Scheduling, Dependencies, SLA, Retries)
- Git, Jupyter Notebook
  
## Architecture
- Extraction: Ingest raw retail data (UCI dataset + Faker-generated synthetic customer data).
- Cleaning: Handle nulls, invalid types, duplicates via Pandas.
- Transformation: Calculate KPIs — RFM segmentation, monthly revenue, country-wise trends.
- Loading: Insert cleaned data into MySQL via SQLAlchemy.
- Orchestration: Apache Airflow DAG handles:
  - Task dependencies
  - Retries
  - SLA Monitoring
  - Failure Handling
  - Daily Scheduling
  - Analysis: Streamlit dashboards for business KPIs & customer insights.

## DAG Structure
  extract → clean → transform → load → analysis

## Airflow Features Implemented
- DAG scheduling: Daily jobs
- Retries with retry delays
- SLA monitoring
- Task dependencies with PythonOperator
- Full modular code organization
- Error handling and logging
  
---

## Streamlit Features
- Interactive Key Metrics (Revenue, Orders, Customers)
- Dynamic filtering by country & timeframe
- Revenue Trends & Top Products visualization
- RFM-based Customer Segmentation
- Top Customers listing
- Country-wise customer distribution
- Dataset Explorer with expanders

## 📁 Folder Structure
retail-analytics-pipeline/
├── airflow-docker/dags # Airflow DAG files
├── data/ # Raw to processed data
├── scripts/ # Master ETL Scripts
├── utils/ # Cleaning and Transformation Script
├── notebooks/ # EDA and visual insights
├── requirements.txt
├── README.md
└── .gitignore

---

## 🧱 Medallion Architecture Overview

- **Bronze**: Raw data from UCI & Faker-generated customer/inventory
- **Silver**: Cleaned and validated data (email, phone, signup date, product info)
- **Gold**: Enriched data with RFM segmentation, monthly sales, country-wise analysis

---

## 📊 Business Insights

1. 📦 **Top 10 Products by Sales**  
2. 📈 **Monthly Revenue Trends** (last 6 months)  
3. 🌍 **Top Countries by Avg Order Value**  
4. 🇳🇴 **Norway’s Favorite Products**  
5. 👥 **Customer Segments using RFM**

All visualizations and insights are available in the notebook:  
📒 [`notebooks/retail_eda_and_insights.ipynb`](notebooks/retail_eda_and_insights.ipynb)

---

## 🧠 Customer Segmentation (RFM)

- **Champions**: Recent, frequent, high spenders
- **Loyal Customers**
- **At Risk**
- **Hibernating**
- And more...

RFM scores are calculated, combined, and used to assign meaningful segments.

---

## 🚀 How to Run

1. Clone the repo:
```bash
git clone https://github.com/yourusername/retail-analytics-pipeline.git

2. Create a virtual environment and install dependencies:

pip install -r requirements.txt

3. Launch app
streamlit run streamlit_app.py

4. Run ETL pipeline:

python scripts/etl_pipeline.py

5. Open Jupyter Notebook for insights:

jupyter notebook notebooks/retail_eda_and_insights.ipynb

6. Insights Section
```markdown
## 📊 Dashboard Insights

1. **Key Metrics**: Revenue, Orders, Customers for filtered timeframe  
2. **Monthly Revenue Trend** chart  
3. **Top 10 Products** bar chart  
4. **Customer Segmentation** via RFM (Champions, Loyal, etc.)  
5. **Top 10 Customers** by spending  
6. **Country Distribution** of unique customers 

📷 Sample Visualizations
### 🥇 Top 10 Products by Total Sales
![Top Products](reports/plots/top_products_sales.png)

### 📈 Monthly Revenue Trend
![Monthly Revenue](reports/plots/monthly_revenue_trend.png)

### 👥 Customer Segmentation (RFM)
![RFM Segments](reports/plots/customer_segments_rfm.png)

🙋‍♀️ About the Author
Built with ❤️ by Payal Goyal, an aspiring Data Engineer passionate about building production-grade analytics pipelines.

📌 License
This project is for educational purposes.
