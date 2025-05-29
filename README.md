# 🛍️ Retail Analytics Data Pipeline (Medallion Architecture)

This project demonstrates an end-to-end retail data analytics pipeline using the Medallion Architecture (Bronze → Silver → Gold) built on the UCI Online Retail dataset.

---

## 🔧 Tech Stack

- **Python** (Pandas, NumPy)
- **MySQL** for gold-layer storage
- **Seaborn / Matplotlib** for visualization
- **Medallion Architecture**: Bronze → Silver → Gold
- **SQLAlchemy** for database connection
- **Jupyter Notebook** for EDA & Insights

---

## 📁 Folder Structure
retail-analytics-pipeline/
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

3. Run ETL pipeline:

python scripts/etl_pipeline.py

4. Open Jupyter Notebook for insights:

jupyter notebook notebooks/retail_eda_and_insights.ipynb


🙋‍♀️ About the Author
Built with ❤️ by Payal Goyal, an aspiring Data Engineer passionate about building production-grade analytics pipelines.

📌 License
This project is for educational purposes.




