import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
import numpy as np
import os

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10

output_dir = 'Task_3_HR_Analytics/dashboard/dashboard_screenshots'
os.makedirs(output_dir, exist_ok=True)

df = pd.read_csv('Task_3_HR_Analytics/data/cleaned_hr_analytics_dataset.csv')

# 1. KPI Summary Banner
fig, ax = plt.subplots(figsize=(14, 2.5), facecolor='#F8FAFC')
ax.axis('off')

kpis = [
    ("TOTAL HEADCOUNT", f"{len(df):,}", "#1E3A8A", "Total Workforce"),
    ("ACTIVE STAFF", f"{(df['Attrition']=='No').sum():,}", "#059669", f"{(df['Attrition']=='No').mean()*100:.1f}% Retained"),
    ("ATTRITION RATE", f"{(df['Attrition']=='Yes').mean()*100:.1f}%", "#DC2626", f"{(df['Attrition']=='Yes').sum()} Exited"),
    ("AVG SALARY", f"${df['MonthlyIncome'].mean():,.0f}", "#7C3AED", "Monthly Baseline"),
    ("AVG ATTENDANCE", f"{df['AttendanceRate'].mean():.1f}%", "#0284C7", f"{df['LeaveDaysTaken'].mean():.1f} Avg Leaves"),
    ("SATISFACTION", f"{df['OverallSatisfaction'].mean():.2f}/4", "#DB2777", "Composite Score")
]

for i, (title, val, color, sub) in enumerate(kpis):
    x_pos = 0.02 + i * 0.165
    rect = patches.FancyBboxPatch(
        (x_pos, 0.08), 0.15, 0.84, transform=ax.transAxes,
        facecolor='white', edgecolor='#E2E8F0', linewidth=1.5,
        boxstyle="round,pad=0.02"
    )
    ax.add_patch(rect)
    ax.text(x_pos + 0.075, 0.72, title, transform=ax.transAxes, ha='center', va='center',
            fontsize=9, weight='bold', color='#64748B')
    ax.text(x_pos + 0.075, 0.45, val, transform=ax.transAxes, ha='center', va='center',
            fontsize=17, weight='bold', color=color)
    ax.text(x_pos + 0.075, 0.20, sub, transform=ax.transAxes, ha='center', va='center',
            fontsize=8.5, weight='bold', color='#475569')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'kpi_summary_banner.png'), dpi=300, bbox_inches='tight', facecolor='#F8FAFC')
plt.close()

# 2. Department Breakdown
fig, ax = plt.subplots(figsize=(8, 4.5), facecolor='#FFFFFF')
dept_data = df.groupby(['Department', 'Attrition']).size().unstack(fill_value=0)
dept_data.plot(kind='bar', stacked=True, color=['#3B82F6', '#EF4444'], ax=ax, width=0.55)
ax.set_title("Department Headcount & Attrition Distribution", fontsize=13, weight='bold', color='#1E293B', pad=12)
ax.set_xlabel("Department", fontsize=11, weight='bold', color='#475569')
ax.set_ylabel("Number of Employees", fontsize=11, weight='bold', color='#475569')
ax.legend(['Active Staff', 'Attrited Staff'], frameon=True, loc='upper right')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'department_attrition_breakdown.png'), dpi=300, bbox_inches='tight')
plt.close()

# 3. Overtime Impact
fig, ax = plt.subplots(figsize=(6, 4.5), facecolor='#FFFFFF')
ot_data = df.groupby('OverTime')['Attrition'].apply(lambda x: (x == 'Yes').mean() * 100).reset_index()
bars = ax.bar(ot_data['OverTime'], ot_data['Attrition'], color=['#3B82F6', '#EF4444'], width=0.45)
ax.set_title("Attrition Rate: Overtime vs No Overtime", fontsize=13, weight='bold', color='#1E293B', pad=12)
ax.set_ylabel("Attrition Rate (%)", fontsize=11, weight='bold', color='#475569')
ax.set_xlabel("OverTime Requirement", fontsize=11, weight='bold', color='#475569')
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.0, yval + 0.8, f"{yval:.1f}%", ha='center', va='bottom', fontsize=11, weight='bold')
ax.set_ylim(0, max(ot_data['Attrition']) + 8)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'overtime_attrition_impact.png'), dpi=300, bbox_inches='tight')
plt.close()

# 4. Attrition by Job Role
fig, ax = plt.subplots(figsize=(9, 5), facecolor='#FFFFFF')
role_data = df.groupby('JobRole')['Attrition'].apply(lambda x: (x == 'Yes').mean() * 100).sort_values()
role_bars = ax.barh(role_data.index, role_data.values, color='#F87171', edgecolor='#DC2626', height=0.6)
ax.set_title("Attrition Rate (%) by Job Role", fontsize=13, weight='bold', color='#1E293B', pad=12)
ax.set_xlabel("Attrition Rate (%)", fontsize=11, weight='bold', color='#475569')
for bar in role_bars:
    xval = bar.get_width()
    ax.text(xval + 0.4, bar.get_y() + bar.get_height()/2.0, f"{xval:.1f}%", ha='left', va='center', fontsize=9.5, weight='bold')
ax.set_xlim(0, max(role_data.values) + 6)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'job_role_attrition.png'), dpi=300, bbox_inches='tight')
plt.close()

# 5. Salary vs Experience
fig, ax = plt.subplots(figsize=(8.5, 4.8), facecolor='#FFFFFF')
sns.scatterplot(
    data=df,
    x='TotalWorkingYears',
    y='MonthlyIncome',
    hue='Attrition',
    palette={'No': '#3B82F6', 'Yes': '#EF4444'},
    alpha=0.75,
    s=45,
    ax=ax
)
ax.set_title("Monthly Income vs Total Experience (Colored by Attrition)", fontsize=13, weight='bold', color='#1E293B', pad=12)
ax.set_xlabel("Total Working Experience (Years)", fontsize=11, weight='bold', color='#475569')
ax.set_ylabel("Monthly Income ($)", fontsize=11, weight='bold', color='#475569')
ax.legend(title='Attrition', frameon=True)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'salary_vs_experience.png'), dpi=300, bbox_inches='tight')
plt.close()

# 6. Promotion Stagnation vs Attrition
fig, ax = plt.subplots(figsize=(8, 4.5), facecolor='#FFFFFF')
promo_data = df.groupby('YearsSinceLastPromotion')['Attrition'].apply(lambda x: (x == 'Yes').mean() * 100)
ax.plot(promo_data.index, promo_data.values, marker='o', linewidth=2.5, color='#DC2626', markersize=6)
ax.set_title("Attrition Probability vs Years Since Last Promotion", fontsize=13, weight='bold', color='#1E293B', pad=12)
ax.set_xlabel("Years Since Last Promotion", fontsize=11, weight='bold', color='#475569')
ax.set_ylabel("Attrition Rate (%)", fontsize=11, weight='bold', color='#475569')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'promotion_stagnation.png'), dpi=300, bbox_inches='tight')
plt.close()

print("All dashboard charts generated successfully in dashboard/dashboard_screenshots/")
