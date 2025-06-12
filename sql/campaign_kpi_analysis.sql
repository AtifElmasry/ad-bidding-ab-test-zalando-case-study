
-- campaign_kpi_analysis.sql
-- SQL queries to analyze A/B bidding strategy test in performance marketing
-- Designed to simulate real-world analysis at companies like Zalando

-- 1. KPI Summary by Group (CTR, CVR, ROAS, CAC)
SELECT 
  group_type,
  ROUND(AVG(clicks * 1.0 / impressions), 4) AS avg_ctr,
  ROUND(AVG(conversions * 1.0 / clicks), 4) AS avg_cvr,
  ROUND(SUM(`revenue (€)`) / SUM(`spend (€)`), 2) AS total_roas,
  ROUND(SUM(`spend (€)`) / NULLIF(SUM(conversions), 0), 2) AS total_cac
FROM ad_data
GROUP BY group_type;

-- 2. Daily Conversion Trend by Group
SELECT 
  date,
  group_type,
  SUM(conversions) AS daily_conversions
FROM ad_data
GROUP BY date, group_type
ORDER BY date;

-- 3. Top 5 Campaigns by ROAS
SELECT 
  campaign_id,
  group_type,
  ROUND(`revenue (€)` / `spend (€)`, 2) AS roas,
  ROUND(conversions * 1.0 / clicks, 4) AS cvr
FROM ad_data
WHERE clicks > 0 AND `spend (€)` > 0
ORDER BY roas DESC
LIMIT 5;

-- 4. Underperforming Campaigns (low revenue or zero conversions)
SELECT 
  campaign_id,
  group_type,
  conversions,
  `spend (€)`,
  `revenue (€)`
FROM ad_data
WHERE conversions = 0 OR `revenue (€)` < 100
ORDER BY `revenue (€)` ASC;

-- 5. Funnel Summary: Impressions -> Clicks -> Conversions by Group
SELECT 
  group_type,
  SUM(impressions) AS total_impressions,
  SUM(clicks) AS total_clicks,
  SUM(conversions) AS total_conversions,
  ROUND(SUM(clicks) * 1.0 / SUM(impressions), 4) AS ctr,
  ROUND(SUM(conversions) * 1.0 / SUM(clicks), 4) AS cvr
FROM ad_data
GROUP BY group_type;
