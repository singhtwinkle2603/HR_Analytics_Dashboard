import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# Set page configuration
st.set_page_config(
    page_title="HR Workforce Analytics & Attrition Intelligence Dashboard",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 30px;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 15px;
        color: #64748B;
        margin-bottom: 20px;
    }
    .kpi-card {
        background: #FFFFFF;
        border-radius: 10px;
        padding: 16px 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        border-left: 5px solid #3B82F6;
        margin-bottom: 12px;
    }
    .kpi-title {
        font-size: 13px;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
    }
    .kpi-value {
        font-size: 26px;
        font-weight: 700;
        color: #0F172A;
    }
    .kpi-sub {
        font-size: 12px;
        color: #10B981;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# Load Data
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, '..', 'data', 'cleaned_hr_analytics_dataset.csv')
    if not os.path.exists(data_path):
        data_path = 'Task_3_HR_Analytics/data/cleaned_hr_analytics_dataset.csv'
    df = pd.read_csv(data_path)
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()

# -----------------------------------------------------------------------------
# SIDEBAR FILTERS
# -----------------------------------------------------------------------------
st.sidebar.image("https://img.icons8.com/fluency/96/conference-call.png", width=70)
st.sidebar.title("🎛️ Filter Panel")
st.sidebar.markdown("Filter workforce metrics dynamically:")

dept_options = ['All'] + sorted(list(df['Department'].unique()))
selected_dept = st.sidebar.selectbox("🏢 Select Department", dept_options)

role_options = sorted(list(df['JobRole'].unique()))
if selected_dept != 'All':
    role_options = sorted(list(df[df['Department'] == selected_dept]['JobRole'].unique()))
selected_roles = st.sidebar.multiselect("💼 Filter by Job Role(s)", role_options, default=role_options)

overtime_filter = st.sidebar.radio("⏱️ Overtime Status", ['All', 'Yes', 'No'], horizontal=True)

age_range = st.sidebar.slider(
    "🎂 Age Range",
    int(df['Age'].min()), int(df['Age'].max()),
    (int(df['Age'].min()), int(df['Age'].max()))
)

salary_range = st.sidebar.slider(
    "💵 Monthly Income ($)",
    int(df['MonthlyIncome'].min()), int(df['MonthlyIncome'].max()),
    (int(df['MonthlyIncome'].min()), int(df['MonthlyIncome'].max())),
    step=500
)

# Apply Filters
filtered_df = df.copy()
if selected_dept != 'All':
    filtered_df = filtered_df[filtered_df['Department'] == selected_dept]
if selected_roles:
    filtered_df = filtered_df[filtered_df['JobRole'].isin(selected_roles)]
if overtime_filter != 'All':
    filtered_df = filtered_df[filtered_df['OverTime'] == overtime_filter]
filtered_df = filtered_df[
    (filtered_df['Age'] >= age_range[0]) & (filtered_df['Age'] <= age_range[1]) &
    (filtered_df['MonthlyIncome'] >= salary_range[0]) & (filtered_df['MonthlyIncome'] <= salary_range[1])
]

# Header Title
st.markdown("<p class='main-header'>👥 HR Workforce Intelligence & Analytics Dashboard</p>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>Executive human capital insights, retention drivers, attendance dynamics, and performance tracking</p>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# KPI METRICS RIBBON
# -----------------------------------------------------------------------------
total_emp = len(filtered_df)
active_emp = (filtered_df['Attrition'] == 'No').sum()
attrition_count = (filtered_df['Attrition'] == 'Yes').sum()
attrition_rate = (attrition_count / total_emp * 100) if total_emp > 0 else 0.0
avg_salary = filtered_df['MonthlyIncome'].mean() if total_emp > 0 else 0.0
avg_attendance = filtered_df['AttendanceRate'].mean() if total_emp > 0 else 0.0
avg_satisfaction = filtered_df['OverallSatisfaction'].mean() if total_emp > 0 else 0.0

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.markdown(f"""
    <div class='kpi-card' style='border-left-color: #3B82F6;'>
        <div class='kpi-title'>Total Headcount</div>
        <div class='kpi-value'>{total_emp:,}</div>
        <div class='kpi-sub' style='color:#3B82F6'>Workforce Size</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='kpi-card' style='border-left-color: #10B981;'>
        <div class='kpi-title'>Active Staff</div>
        <div class='kpi-value'>{active_emp:,}</div>
        <div class='kpi-sub'>{(active_emp/total_emp*100):.1f}% Retained</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    attr_color = "#EF4444" if attrition_rate > 15 else "#F59E0B"
    st.markdown(f"""
    <div class='kpi-card' style='border-left-color: {attr_color};'>
        <div class='kpi-title'>Attrition Rate</div>
        <div class='kpi-value' style='color:{attr_color};'>{attrition_rate:.1f}%</div>
        <div class='kpi-sub' style='color:{attr_color};'>{attrition_count} Departures</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class='kpi-card' style='border-left-color: #8B5CF6;'>
        <div class='kpi-title'>Avg Monthly Income</div>
        <div class='kpi-value'>${avg_salary:,.0f}</div>
        <div class='kpi-sub' style='color:#8B5CF6'>Industry Baseline</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class='kpi-card' style='border-left-color: #06B6D4;'>
        <div class='kpi-title'>Avg Attendance</div>
        <div class='kpi-value'>{avg_attendance:.1f}%</div>
        <div class='kpi-sub' style='color:#06B6D4'>{filtered_df['LeaveDaysTaken'].mean():.1f} Avg Leaves</div>
    </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown(f"""
    <div class='kpi-card' style='border-left-color: #EC4899;'>
        <div class='kpi-title'>Satisfaction Index</div>
        <div class='kpi-value'>{avg_satisfaction:.2f}<span style='font-size:16px;color:#94A3B8'>/4.0</span></div>
        <div class='kpi-sub' style='color:#EC4899'>Composite Score</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# DASHBOARD TABS
# -----------------------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Executive Summary",
    "🚨 Attrition Intelligence",
    "💰 Compensation & Performance",
    "📅 Attendance & Wellbeing",
    "🔍 High-Risk Employee Explorer"
])

# -----------------------------------------------------------------------------
# TAB 1: EXECUTIVE SUMMARY
# -----------------------------------------------------------------------------
with tab1:
    col_t1_a, col_t1_b = st.columns([6, 4])
    
    with col_t1_a:
        st.subheader("🏢 Department Headcount & Attrition Rate")
        dept_summary = filtered_df.groupby('Department').agg(
            Total=('EmployeeID', 'count'),
            Attrition=('AttritionCount', 'sum')
        ).reset_index()
        dept_summary['AttritionRate'] = dept_summary['Attrition'] / dept_summary['Total'] * 100
        dept_summary['Active'] = dept_summary['Total'] - dept_summary['Attrition']
        
        fig_dept = go.Figure()
        fig_dept.add_trace(go.Bar(
            name='Active Staff',
            x=dept_summary['Department'],
            y=dept_summary['Active'],
            marker_color='#3B82F6'
        ))
        fig_dept.add_trace(go.Bar(
            name='Attrited Staff',
            x=dept_summary['Department'],
            y=dept_summary['Attrition'],
            marker_color='#EF4444'
        ))
        fig_dept.update_layout(
            barmode='stack',
            height=350,
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_dept, use_container_width=True)

    with col_t1_b:
        st.subheader("🎯 Attrition by Age Demographics")
        age_dist = filtered_df.groupby('AgeGroup', observed=False).agg(
            Total=('EmployeeID', 'count'),
            Attrition=('AttritionCount', 'sum')
        ).reset_index()
        age_dist['AttritionRate'] = age_dist['Attrition'] / age_dist['Total'] * 100

        fig_age = px.pie(
            age_dist,
            values='Attrition',
            names='AgeGroup',
            hole=0.45,
            color_discrete_sequence=px.colors.sequential.RdBu_r
        )
        fig_age.update_layout(height=350, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig_age, use_container_width=True)

    col_t1_c, col_t1_d = st.columns([5, 5])
    with col_t1_c:
        st.subheader("🧭 Business Travel vs Attrition")
        travel_summary = filtered_df.groupby(['BusinessTravel', 'Attrition'], observed=False).size().reset_index(name='Count')
        fig_travel = px.bar(
            travel_summary,
            x='BusinessTravel',
            y='Count',
            color='Attrition',
            barmode='group',
            color_discrete_map={'No': '#10B981', 'Yes': '#EF4444'}
        )
        fig_travel.update_layout(height=320, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig_travel, use_container_width=True)

    with col_t1_d:
        st.subheader("💼 Education Field Breakdown")
        edu_summary = filtered_df.groupby('EducationField').size().reset_index(name='Headcount')
        fig_edu = px.bar(
            edu_summary.sort_values('Headcount', ascending=True),
            x='Headcount',
            y='EducationField',
            orientation='h',
            color='Headcount',
            color_continuous_scale='Blues'
        )
        fig_edu.update_layout(height=320, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig_edu, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 2: ATTRITION INTELLIGENCE
# -----------------------------------------------------------------------------
with tab2:
    st.subheader("🚨 Root-Cause Analysis of Workforce Attrition")
    
    col_t2_a, col_t2_b = st.columns(2)
    with col_t2_a:
        st.markdown("**1. Impact of Overtime on Attrition**")
        ot_data = filtered_df.groupby(['OverTime'], observed=False).agg(
            Total=('EmployeeID', 'count'),
            Resigned=('AttritionCount', 'sum')
        ).reset_index()
        ot_data['AttritionRate'] = ot_data['Resigned'] / ot_data['Total'] * 100
        
        fig_ot = px.bar(
            ot_data,
            x='OverTime',
            y='AttritionRate',
            text=ot_data['AttritionRate'].apply(lambda x: f"{x:.1f}%"),
            color='OverTime',
            color_discrete_map={'Yes': '#EF4444', 'No': '#3B82F6'},
            labels={'AttritionRate': 'Attrition Rate (%)', 'OverTime': 'Overtime Required'}
        )
        fig_ot.update_layout(height=320, showlegend=False)
        st.plotly_chart(fig_ot, use_container_width=True)

    with col_t2_b:
        st.markdown("**2. Commute Distance Impact on Resignations**")
        fig_commute = px.histogram(
            filtered_df,
            x='DistanceFromHome',
            color='Attrition',
            barmode='overlay',
            nbins=25,
            color_discrete_map={'No': '#93C5FD', 'Yes': '#EF4444'},
            labels={'DistanceFromHome': 'Distance From Home (KM)'}
        )
        fig_commute.update_layout(height=320)
        st.plotly_chart(fig_commute, use_container_width=True)

    col_t2_c, col_t2_d = st.columns(2)
    with col_t2_c:
        st.markdown("**3. Attrition Rate by Job Role**")
        role_attr = filtered_df.groupby('JobRole').agg(
            Total=('EmployeeID', 'count'),
            Resigned=('AttritionCount', 'sum')
        ).reset_index()
        role_attr['AttritionRate'] = role_attr['Resigned'] / role_attr['Total'] * 100
        role_attr = role_attr.sort_values('AttritionRate', ascending=True)

        fig_role = px.bar(
            role_attr,
            x='AttritionRate',
            y='JobRole',
            orientation='h',
            color='AttritionRate',
            color_continuous_scale='Reds',
            text=role_attr['AttritionRate'].apply(lambda x: f"{x:.1f}%")
        )
        fig_role.update_layout(height=360)
        st.plotly_chart(fig_role, use_container_width=True)

    with col_t2_d:
        st.markdown("**4. Years Since Last Promotion vs Resignations**")
        promo_attr = filtered_df.groupby('YearsSinceLastPromotion').agg(
            Total=('EmployeeID', 'count'),
            Resigned=('AttritionCount', 'sum')
        ).reset_index()
        promo_attr['AttritionRate'] = promo_attr['Resigned'] / promo_attr['Total'] * 100

        fig_promo = px.line(
            promo_attr,
            x='YearsSinceLastPromotion',
            y='AttritionRate',
            markers=True,
            line_shape='spline',
            color_discrete_sequence=['#DC2626']
        )
        fig_promo.update_layout(height=360, yaxis_title="Attrition Rate (%)", xaxis_title="Years Stagnant Without Promotion")
        st.plotly_chart(fig_promo, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 3: COMPENSATION & PERFORMANCE
# -----------------------------------------------------------------------------
with tab3:
    st.subheader("💰 Compensation Distribution & Performance Rating Correlations")
    
    col_t3_a, col_t3_b = st.columns([6, 4])
    with col_t3_a:
        st.markdown("**Monthly Salary Distribution Across Job Roles**")
        fig_sal = px.box(
            filtered_df,
            x='MonthlyIncome',
            y='JobRole',
            color='JobRole',
            points='outliers'
        )
        fig_sal.update_layout(height=380, showlegend=False)
        st.plotly_chart(fig_sal, use_container_width=True)

    with col_t3_b:
        st.markdown("**Salary Slab vs Attrition Probability**")
        slab_attr = filtered_df.groupby('SalarySlab', observed=False).agg(
            Total=('EmployeeID', 'count'),
            Resigned=('AttritionCount', 'sum'),
            AvgHike=('PercentSalaryHike', 'mean')
        ).reset_index()
        slab_attr['AttritionRate'] = slab_attr['Resigned'] / slab_attr['Total'] * 100

        fig_slab = px.bar(
            slab_attr,
            x='SalarySlab',
            y='AttritionRate',
            color='AttritionRate',
            color_continuous_scale='Oranges',
            text=slab_attr['AttritionRate'].apply(lambda x: f"{x:.1f}%")
        )
        fig_slab.update_layout(height=380)
        st.plotly_chart(fig_slab, use_container_width=True)

    col_t3_c, col_t3_d = st.columns(2)
    with col_t3_c:
        st.markdown("**Total Working Experience vs Monthly Income (Colored by Attrition)**")
        fig_scatter = px.scatter(
            filtered_df,
            x='TotalWorkingYears',
            y='MonthlyIncome',
            color='Attrition',
            size='YearsAtCompany',
            hover_data=['JobRole', 'Age'],
            color_discrete_map={'No': '#3B82F6', 'Yes': '#EF4444'}
        )
        fig_scatter.update_layout(height=350)
        st.plotly_chart(fig_scatter, use_container_width=True)

    with col_t3_d:
        st.markdown("**Gender Pay Equity Across Departments**")
        gender_pay = filtered_df.groupby(['Department', 'Gender']).agg(
            AvgSalary=('MonthlyIncome', 'mean'),
            AvgHike=('PercentSalaryHike', 'mean')
        ).reset_index()
        fig_gender = px.bar(
            gender_pay,
            x='Department',
            y='AvgSalary',
            color='Gender',
            barmode='group',
            color_discrete_sequence=['#3B82F6', '#EC4899']
        )
        fig_gender.update_layout(height=350, yaxis_title="Average Monthly Salary ($)")
        st.plotly_chart(fig_gender, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 4: ATTENDANCE & WELLBEING
# -----------------------------------------------------------------------------
with tab4:
    st.subheader("📅 Attendance, Leave Analytics & Wellbeing Dynamics")
    
    col_t4_a, col_t4_b = st.columns(2)
    with col_t4_a:
        st.markdown("**Attendance Rate Distribution by Work-Life Balance Rating**")
        fig_att = px.violin(
            filtered_df,
            x='WorkLifeBalance',
            y='AttendanceRate',
            color='WorkLifeBalance',
            box=True,
            points='all',
            color_discrete_sequence=px.colors.sequential.Teal
        )
        fig_att.update_layout(height=350, showlegend=False, xaxis_title="Work-Life Balance Rating (1=Poor, 4=Best)")
        st.plotly_chart(fig_att, use_container_width=True)

    with col_t4_b:
        st.markdown("**Leaves Taken vs Overall Job Satisfaction**")
        fig_leave = px.box(
            filtered_df,
            x='JobSatisfaction',
            y='LeaveDaysTaken',
            color='JobSatisfaction',
            color_discrete_sequence=px.colors.sequential.Viridis
        )
        fig_leave.update_layout(height=350, showlegend=False, xaxis_title="Job Satisfaction (1=Low, 4=High)", yaxis_title="Annual Leaves Taken")
        st.plotly_chart(fig_leave, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 5: HIGH-RISK EMPLOYEE EXPLORER
# -----------------------------------------------------------------------------
with tab5:
    st.subheader("🔍 Early Warning: High Attrition Risk Employees")
    st.markdown("Filter staff exhibiting high-risk factors: **OverTime = Yes**, **Job Satisfaction <= 2**, **Monthly Income < $5,000**, or **Promotion Stagnation >= 4 years**.")
    
    risk_condition = (
        (filtered_df['OverTime'] == 'Yes') |
        (filtered_df['JobSatisfaction'] <= 2) |
        (filtered_df['MonthlyIncome'] < 4000) |
        (filtered_df['YearsSinceLastPromotion'] >= 4)
    )
    
    high_risk_df = filtered_df[risk_condition].copy()
    high_risk_df['RiskScore'] = (
        (high_risk_df['OverTime'] == 'Yes').astype(int)*30 +
        (high_risk_df['JobSatisfaction'] <= 2).astype(int)*25 +
        (high_risk_df['MonthlyIncome'] < 4000).astype(int)*25 +
        (high_risk_df['YearsSinceLastPromotion'] >= 4).astype(int)*20
    )
    
    display_cols = [
        'EmployeeID', 'JobRole', 'Department', 'MonthlyIncome', 'OverTime',
        'JobSatisfaction', 'WorkLifeBalance', 'YearsSinceLastPromotion', 'AttendanceRate', 'Attrition', 'RiskScore'
    ]
    
    st.dataframe(
        high_risk_df[display_cols].sort_values('RiskScore', ascending=False),
        use_container_width=True,
        hide_index=True
    )
    
    # Download Button
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Current Filtered Dataset (CSV)",
        data=csv,
        file_name='hr_analytics_filtered_data.csv',
        mime='text/csv'
    )
