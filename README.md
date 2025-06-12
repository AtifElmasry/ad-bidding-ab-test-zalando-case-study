# 🎯 Ad Bidding A/B Test – Zalando Case Study

This is a fun and realistic A/B testing project where I analyze how two different ad bidding strategies—manual vs automated—perform across core marketing KPIs.

It's designed to reflect the kind of work a data analyst might do at a performance-driven company like **Zalando**.

---

## 🧪 What’s the Goal?

We want to see which bidding strategy works better based on:

- 📈 CTR: Click-Through Rate
- ✅ CVR: Conversion Rate
- 💸 ROAS: Return on Ad Spend
- 🧮 CAC: Customer Acquisition Cost

---

## 🛠️ What Did I Use?

- **Python** – for data analysis, visualizations, and A/B test checks.
- **SQL (MySQL)** – to crunch campaign metrics.
- **Jupyter Notebook** – to walk through the whole analysis.
- **MySQL Workbench** – for SQL queries and KPIs.

---

## 📁 Folder Tour

```
project/
├── data/           → Clean campaign dataset (.csv)
├── scripts/        → Python script to generate dummy data
├── notebooks/      → Main Jupyter analysis notebook
├── outputs/        → Visualizations saved as .png
├── sql/            → SQL query for KPI aggregation
├── README.md       → You’re reading it :)
```

---

## 🔍 Insights I Found

- ROAS and CAC were **pretty close** between the two groups.
- The **test group (automated bidding)** had more variability in conversions, but peaked early.
- **Manual bidding** had a few standout campaigns (best ROAS), but overall the results were mixed.
- This suggests that a **hybrid approach** might be worth exploring.

---

## 🧠 Example SQL Query I Ran

```sql
SELECT
  group_type,
  ROUND(SUM(clicks) / SUM(impressions), 4) AS CTR,
  ROUND(SUM(conversions) / SUM(clicks), 4) AS CVR,
  ROUND(SUM(revenue_eur) / SUM(spend_eur), 2) AS ROAS,
  ROUND(SUM(spend_eur) / SUM(conversions), 2) AS CAC
FROM ad_data
GROUP BY group_type;
```

---

## 📸 Some Visuals I Made

### ROAS & CAC Boxplots
![ROAS and CAC comparison](outputs/roas_cac_comparison.png)

### Daily Conversions Trend
![Daily conversions](outputs/daily_conversions.png)

### Top 5 Campaigns by ROAS
![Top 5 campaigns](outputs/top5_campaigns_roas.png)

### ROAS by Group Type
![ROAS by group type](outputs/roas_by_group_boxplot.png)

---

## ▶️ How to Try It Yourself

1. Clone the repo
2. Run `pip install -r requirements.txt`
3. Open `notebooks/analysis.ipynb`
4. Or, explore the SQL in `sql/campaign_kpi_analysis.sql`

---

## ✍️ About Me

**Atif Elmasry**  
Product & Data Analyst | SQL + Python | Performance Marketing  
📍 Based in Berlin  
📫 Find me on [LinkedIn](https://www.linkedin.com/in/tioatifelmasry)

---

> If you're a hiring manager or interviewer, I’d love to walk you through this project live and talk through my thought process.