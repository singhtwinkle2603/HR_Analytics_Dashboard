-- =============================================================================
-- Task 3: HR Analytics Dashboard - Database Schema & Table Definitions
-- Dialect: ANSI SQL / PostgreSQL / MySQL Compatible
-- Description: Defines staging and normalized tables for Employee HR data
-- =============================================================================

CREATE TABLE IF NOT EXISTS hr_employees (
    employee_id                 VARCHAR(20) PRIMARY KEY,
    age                         INT NOT NULL,
    attrition                   VARCHAR(10) NOT NULL, -- 'Yes' or 'No'
    business_travel             VARCHAR(30),          -- 'Non-Travel', 'Travel_Rarely', 'Travel_Frequently'
    department                  VARCHAR(50) NOT NULL, -- 'Sales', 'Research & Development', 'Human Resources'
    distance_from_home          INT,                  -- Distance in KM
    education_field             VARCHAR(50),
    environment_satisfaction    INT CHECK (environment_satisfaction BETWEEN 1 AND 4),
    gender                      VARCHAR(10),
    job_role                    VARCHAR(50) NOT NULL,
    job_satisfaction            INT CHECK (job_satisfaction BETWEEN 1 AND 4),
    marital_status              VARCHAR(20),
    monthly_income              DECIMAL(10, 2) NOT NULL,
    num_companies_worked        INT,
    over_time                   VARCHAR(5),           -- 'Yes' or 'No'
    percent_salary_hike         DECIMAL(5, 2),
    performance_rating          INT CHECK (performance_rating BETWEEN 1 AND 5),
    relationship_satisfaction   INT CHECK (relationship_satisfaction BETWEEN 1 AND 4),
    stock_option_level          INT CHECK (stock_option_level BETWEEN 0 AND 3),
    total_working_years         INT,
    training_times_last_year    INT,
    work_life_balance           INT CHECK (work_life_balance BETWEEN 1 AND 4),
    years_at_company            INT,
    years_in_current_role       INT,
    years_since_last_promotion  INT,
    years_with_curr_manager     INT,
    attendance_rate             DECIMAL(5, 2),        -- Percentage (e.g. 94.50)
    leave_days_taken            INT,
    created_at                  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indices for rapid dashboard filtering and analytical aggregations
CREATE INDEX idx_hr_department ON hr_employees(department);
CREATE INDEX idx_hr_attrition ON hr_employees(attrition);
CREATE INDEX idx_hr_job_role ON hr_employees(job_role);
CREATE INDEX idx_hr_overtime ON hr_employees(over_time);
CREATE INDEX idx_hr_income ON hr_employees(monthly_income);
