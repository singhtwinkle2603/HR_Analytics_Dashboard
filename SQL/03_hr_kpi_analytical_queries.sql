-- =============================================================================
-- Task 3: HR Analytics Dashboard - Core Analytical & KPI SQL Queries
-- Description: Business Intelligence queries for workforce insights, attrition,
--              attendance, salary distribution, and performance evaluation.
-- =============================================================================

-- -----------------------------------------------------------------------------
-- QUERY 1: Overall HR Organization Health KPIs
-- -----------------------------------------------------------------------------
SELECT 
    COUNT(employee_id)                                         AS total_headcount,
    SUM(CASE WHEN attrition = 'No' THEN 1 ELSE 0 END)          AS active_employees,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END)         AS attrited_employees,
    ROUND(AVG(CASE WHEN attrition = 'Yes' THEN 1.0 ELSE 0.0 END) * 100, 2) AS attrition_rate_pct,
    ROUND(AVG(monthly_income), 2)                              AS avg_monthly_income,
    ROUND(AVG(attendance_rate), 2)                             AS avg_attendance_rate_pct,
    ROUND(AVG(leave_days_taken), 1)                            AS avg_leave_days,
    ROUND(AVG(years_at_company), 1)                            AS avg_tenure_years
FROM hr_employees;


-- -----------------------------------------------------------------------------
-- QUERY 2: Attrition & Headcount Breakdown by Job Role
-- -----------------------------------------------------------------------------
SELECT 
    job_role,
    department,
    COUNT(employee_id) AS total_employees,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS attrited_count,
    ROUND(AVG(CASE WHEN attrition = 'Yes' THEN 1.0 ELSE 0.0 END) * 100, 2) AS attrition_rate_pct,
    ROUND(AVG(monthly_income), 2) AS avg_salary,
    ROUND(AVG(job_satisfaction), 2) AS avg_job_satisfaction
FROM hr_employees
GROUP BY job_role, department
ORDER BY attrition_rate_pct DESC;


-- -----------------------------------------------------------------------------
-- QUERY 3: Impact of Overtime and Work-Life Balance on Employee Attrition
-- -----------------------------------------------------------------------------
SELECT 
    over_time,
    work_life_balance,
    COUNT(employee_id) AS total_employees,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS attrited_count,
    ROUND(AVG(CASE WHEN attrition = 'Yes' THEN 1.0 ELSE 0.0 END) * 100, 2) AS attrition_rate_pct,
    ROUND(AVG(attendance_rate), 2) AS avg_attendance_rate
FROM hr_employees
GROUP BY over_time, work_life_balance
ORDER BY over_time DESC, work_life_balance ASC;


-- -----------------------------------------------------------------------------
-- QUERY 4: Compensation & Salary Slab Attrition Matrix
-- -----------------------------------------------------------------------------
SELECT 
    CASE 
        WHEN monthly_income < 3500 THEN '1. Entry Level (<$3.5k)'
        WHEN monthly_income BETWEEN 3500 AND 7000 THEN '2. Mid Level ($3.5k-$7k)'
        WHEN monthly_income BETWEEN 7001 AND 12000 THEN '3. Senior Level ($7k-$12k)'
        ELSE '4. Executive Level ($12k+)'
    END AS salary_bracket,
    COUNT(employee_id) AS employee_count,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS attrition_count,
    ROUND(AVG(CASE WHEN attrition = 'Yes' THEN 1.0 ELSE 0.0 END) * 100, 2) AS attrition_rate_pct,
    ROUND(AVG(percent_salary_hike), 2) AS avg_hike_pct
FROM hr_employees
GROUP BY 1
ORDER BY 1;


-- -----------------------------------------------------------------------------
-- QUERY 5: Attendance, Leave Patterns & Burnout Risk Analysis
-- -----------------------------------------------------------------------------
SELECT 
    department,
    CASE 
        WHEN attendance_rate >= 95.0 THEN 'High Attendance (>=95%)'
        WHEN attendance_rate BETWEEN 90.0 AND 94.99 THEN 'Standard Attendance (90-95%)'
        ELSE 'Low Attendance (<90%)'
    END AS attendance_category,
    COUNT(employee_id) AS employee_count,
    ROUND(AVG(leave_days_taken), 1) AS avg_leaves,
    ROUND(AVG(CASE WHEN attrition = 'Yes' THEN 1.0 ELSE 0.0 END) * 100, 2) AS attrition_rate_pct
FROM hr_employees
GROUP BY department, 2
ORDER BY department, avg_leaves DESC;


-- -----------------------------------------------------------------------------
-- QUERY 6: Promotion Stagnation vs Employee Retention
-- -----------------------------------------------------------------------------
SELECT 
    years_since_last_promotion,
    COUNT(employee_id) AS total_headcount,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS resigned_count,
    ROUND(AVG(CASE WHEN attrition = 'Yes' THEN 1.0 ELSE 0.0 END) * 100, 2) AS attrition_rate_pct,
    ROUND(AVG(performance_rating), 2) AS avg_performance_rating
FROM hr_employees
GROUP BY years_since_last_promotion
ORDER BY years_since_last_promotion ASC;


-- -----------------------------------------------------------------------------
-- QUERY 7: Gender Diversity & Pay Equity Analysis Across Departments
-- -----------------------------------------------------------------------------
SELECT 
    department,
    gender,
    COUNT(employee_id) AS headcount,
    ROUND(COUNT(employee_id) * 100.0 / SUM(COUNT(employee_id)) OVER(PARTITION BY department), 1) AS gender_representation_pct,
    ROUND(AVG(monthly_income), 2) AS avg_monthly_income,
    ROUND(AVG(percent_salary_hike), 2) AS avg_salary_hike_pct,
    ROUND(AVG(performance_rating), 2) AS avg_performance
FROM hr_employees
GROUP BY department, gender
ORDER BY department, gender;
