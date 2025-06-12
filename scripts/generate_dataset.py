import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

start_date = datetime(2025, 6, 1)
days = 14
campaigns_per_day = 6
data = []

for day in range(days):
    date = start_date + timedelta(days=day)
    for campaign in range(1, campaigns_per_day + 1):
        group_type = 'control' if campaign <= 3 else 'test'
        impressions = np.random.randint(8000, 15000)
        ctr = np.random.uniform(0.03, 0.06)
        clicks = int(impressions * ctr)
        cvr = np.random.uniform(0.04, 0.10)
        conversions = int(clicks * cvr)
        spend = round(clicks * np.random.uniform(0.15, 0.30), 2)
        revenue = round(conversions * np.random.uniform(10, 20), 2)

        data.append([
            date.strftime('%Y-%m-%d'),
            f"{day+1:02d}{campaign:02d}",
            group_type,
            impressions,
            clicks,
            conversions,
            spend,
            revenue
        ])

columns = ['date', 'campaign_id', 'group_type', 'impressions', 'clicks', 'conversions', 'spend (€)', 'revenue (€)']
df = pd.DataFrame(data, columns=columns)
df.to_csv("data/ad_bidding_case_study_data.csv", index=False)
print("✅ Dummy dataset created at: data/ad_bidding_case_study_data.csv")
