# 📊 Power BI & Tableau Implementation Guide: HR Analytics Dashboard

This guide provides the complete blueprint for building the **Task 3: HR Analytics Dashboard** in **Microsoft Power BI** or **Tableau Desktop**, including DAX measures, data modeling relationships, visual layouts, and color palettes.

---

## 1. 🧮 Data Model & DAX Measures (Power BI)

Import `cleaned_hr_analytics_dataset.csv` into Power BI Desktop. Create a dedicated **Measures Table** (`_HR_Measures`) and add the following DAX calculations:

### 🔹 Core Workforce Measures

#### **1. Total Headcount**
```dax
Total Headcount = COUNTROWS('cleaned_hr_analytics_dataset')
```

#### **2. Active Employees**
```dax
Active Employees = 
CALCULATE(
    COUNTROWS('cleaned_hr_analytics_dataset'),
    'cleaned_hr_analytics_dataset'[Attrition] = "No"
)
```

#### **3. Attrition Count (Resigned Employees)**
```dax
Attrition Count = 
CALCULATE(
    COUNTROWS('cleaned_hr_analytics_dataset'),
    'cleaned_hr_analytics_dataset'[Attrition] = "Yes"
)
```

#### **4. Attrition Rate (%)**
```dax
Attrition Rate % = 
DIVIDE([Attrition Count], [Total Headcount], 0) * 100
```

#### **5. Retention Rate (%)**
```dax
Retention Rate % = 
DIVIDE([Active Employees], [Total Headcount], 0) * 100
```

---

### 🔹 Compensation & Performance Measures

#### **6. Average Monthly Income**
```dax
Average Monthly Income = 
AVERAGE('cleaned_hr_analytics_dataset'[MonthlyIncome])
```

#### **7. Average Salary Hike (%)**
```dax
Average Salary Hike % = 
AVERAGE('cleaned_hr_analytics_dataset'[PercentSalaryHike])
```

#### **8. High Performance Headcount (Rating >= 4)**
```dax
High Performers Count = 
CALCULATE(
    COUNTROWS('cleaned_hr_analytics_dataset'),
    'cleaned_hr_analytics_dataset'[PerformanceRating] >= 4
)
```

---

### 🔹 Attendance & Satisfaction Measures

#### **9. Average Attendance Rate (%)**
```dax
Average Attendance Rate % = 
AVERAGE('cleaned_hr_analytics_dataset'[AttendanceRate])
```

#### **10. Average Leave Days Taken**
```dax
Average Leaves Taken = 
AVERAGE('cleaned_hr_analytics_dataset'[LeaveDaysTaken])
```

#### **11. Average Satisfaction Score (1-4 Scale)**
```dax
Avg Job Satisfaction = 
AVERAGE('cleaned_hr_analytics_dataset'[JobSatisfaction])
```

#### **12. Average Work-Life Balance Rating**
```dax
Avg Work-Life Balance = 
AVERAGE('cleaned_hr_analytics_dataset'[WorkLifeBalance])
```

---

## 2. 🎨 Dashboard Layout & Visuals Wireframe

### **Header & KPI Ribbon (Top Row)**
| Visual Type | Field / Measure | Card Color Accent |
|---|---|---|
| **Card (New)** | `[Total Headcount]` | Blue (`#3B82F6`) |
| **Card (New)** | `[Active Employees]` | Green (`#10B981`) |
| **Card (New)** | `[Attrition Rate %]` | Red / Amber (`#EF4444`) |
| **Card (New)** | `[Average Monthly Income]` | Purple (`#8B5CF6`) |
| **Card (New)** | `[Average Attendance Rate %]` | Cyan (`#06B6D4`) |
| **Card (New)** | `[Avg Job Satisfaction]` | Pink (`#EC4899`) |

---

### **Visual Grid (Middle & Bottom Sections)**

1. **Department Breakdown (Stacked Bar Chart)**
   - **X-axis:** `Department`
   - **Y-axis:** `[Active Employees]`, `[Attrition Count]`
   - **Legend:** Status (`Active` vs `Attrited`)

2. **Attrition by Job Role (Clustered Horizontal Bar Chart)**
   - **Y-axis:** `JobRole`
   - **X-axis:** `[Attrition Rate %]`
   - **Data Labels:** Enabled (%)

3. **Overtime Impact on Turnover (100% Stacked Column Chart)**
   - **X-axis:** `OverTime` (`Yes` / `No`)
   - **Y-axis:** `[Total Headcount]`
   - **Legend:** `Attrition`

4. **Commute Distance vs Resignations (Histogram / Column Chart)**
   - **X-axis:** `DistanceFromHome`
   - **Y-axis:** `[Attrition Count]`

5. **Monthly Income vs Total Experience (Scatter Plot)**
   - **X-axis:** `TotalWorkingYears`
   - **Y-axis:** `MonthlyIncome`
   - **Legend:** `Attrition`
   - **Size:** `YearsAtCompany`

6. **Attendance Rate by Work-Life Balance (Violin / Box Plot or Column Chart)**
   - **X-axis:** `WorkLifeBalance` (1=Low to 4=Best)
   - **Y-axis:** `[Average Attendance Rate %]`

---

## 3. 🎛️ Interactive Slicers (Left Panel)
Add vertical slicers for end-user interaction:
- **Department** (Dropdown or Tile)
- **Job Role** (Multi-select list)
- **OverTime** (Toggle / Buttons)
- **Age Group** (`<25`, `25-35`, `36-45`, `46+`)
- **Salary Slab** (`Entry`, `Mid`, `Senior`, `Executive`)

---

## 4. 🎨 Design Color Theme Palette (Hex Codes)
- **Primary Navy:** `#1E3A8A`
- **Active Green:** `#10B981`
- **Attrition Warning Red:** `#EF4444`
- **Accent Purple:** `#8B5CF6`
- **Card Background:** `#FFFFFF`
- **Canvas Background:** `#F8FAFC`
- **Text Main:** `#0F172A`
- **Text Secondary:** `#64748B`
