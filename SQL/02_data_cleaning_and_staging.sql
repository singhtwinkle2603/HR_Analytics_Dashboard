-- =============================================================================
-- Task 3: HR Analytics Dashboard - Data Transformation & Business Views
-- Description: Creates analytical views and categorized dimension columns
-- =============================================================================

-- 1. Analytical View with Derived Dimensions (Age Bracket, Salary Band, Tenure Tier)
CREATE OR REPLACE VIEW vw_hr_employees_enriched AS
SELECT
    employee_id,
    age,
    CASE 
        WHEN age < 25 THEN '<25 Years'
        WHEN age BETWEEN 25 AND 35 THEN '25-35 Years'
        WHEN age BETWEEN 36 AND 45 THEN '36-45 Years'
        ELSE '46+ Years'
    END AS age_group,
    gender,
    marital_status,
    department,
    job_role,
    education_field,
    business_travel,
    distance_from_home,
    CASE 
        WHEN distance_from_home <= 5 THEN 'Near (0-5 km)'
        WHEN distance_from_home BETWEEN 6 AND 15 THEN 'Moderate (6-15 km)'
        ELSE 'Far (>15 km)'
    END AS commute_tier,
    monthly_income,
    CASE 
        WHEN monthly_income < 3500 THEN 'Entry Level (<$3.5k)'
        WHEN monthly_income BETWEEN 3500 AND 7000 THEN 'Mid Level ($3.5k-$7k)'
        WHEN monthly_income BETWEEN 7001 AND 12000 THEN 'Senior Level ($7k-$12k)'
        ELSE 'Executive Level ($12k+)'
    END AS salary_slab,
    percent_salary_hike,
    performance_rating,
    job_satisfaction,
    environment_satisfaction,
    relationship_satisfaction,
    work_life_balance,
    (job_satisfaction + environment_satisfaction + relationship_satisfaction + work_life_balance) / 4.0 AS overall_satisfaction_score,
    over_time,
    total_working_years,
    years_at_company,
    CASE 
        WHEN years_at_company <= 2 THEN '0-2 Years (New)'
        WHEN years_at_company BETWEEN 3 AND 5 THEN '3-5 Years (Mid-Tenure)'
        WHEN years_at_company BETWEEN 6 AND 10 THEN '6-10 Years (Experienced)'
        ELSE '10+ Years (Veteran)'
    END AS tenure_tier,
    years_in_current_role,
    years_since_last_promotion,
    CASE 
        WHEN years_since_last_promotion >= 5 THEN 'Stagnant (5+ Yrs)'
        WHEN years_since_last_promotion BETWEEN 2 AND 4 THEN 'Moderate (2-4 Yrs)'
        ELSE 'Recent (<2 Yrs)'
    END AS promotion_status,
    years_with_curr_manager,
    attendance_rate,
    leave_days_taken,
    attrition,
    CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END AS is_attrited,
    CASE WHEN attrition = 'No' THEN 1 ELSE 0 END AS is_active
FROM hr_employees;

-- 2. Department-level Executive Summary View
CREATE OR REPLACE VIEW vw_hr_department_kpis AS
SELECT 
    department,
    COUNT(employee_id) AS total_headcount,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS total_attrition,
    SUM(CASE WHEN attrition = 'No' THEN 1 ELSE 0 END) AS active_headcount,
    ROUND(AVG(CASE WHEN attrition = 'Yes' THEN 1.0 ELSE 0.0 END) * 100, 2) AS attrition_rate_pct,
    ROUND(AVG(monthly_income), 2) AS avg_monthly_income,
    ROUND(AVG(attendance_rate), 2) AS avg_attendance_rate_pct,
    ROUND(AVG(leave_days_taken), 1) AS avg_leaves_taken,
    ROUND(AVG((job_satisfaction + environment_satisfaction + work_life_balance) / 3.0), 2) AS avg_satisfaction_score
FROM hr_employees
GROUP BY department;
