import pandas as pd
import streamlit as st
import plotly.express as px

# Carregando os dois DataFrames da pasta Data_Categorization
df_part1 = pd.read_csv("Data_Categorization/processed_data_part1.csv")
df_part2 = pd.read_csv("Data_Categorization/processed_data_part2.csv")

# Carregando o DataFrame de causas raízes
df_root_causes = pd.read_csv("Root_Cause_Hypothesis/Touchpoints_Final_Sorted.csv")

# Combinando os dois DataFrames de dados de clientes
df_combined = pd.concat([df_part1, df_part2], ignore_index=True)

def map_category_to_touchpoint(category):
    mapping = {
        'Search and Evaluate Professional Score': 'Search and Evaluate Professional Score',
        'Schedule Appointment': 'Schedule Appointment',
        'Make Payment Online': 'Make Payment Online',
        'Check-in Online': 'Check-in Online',
        'Attend Online Consultation': 'Attend Online Consultation',
        'Attend Offline Consultation': 'Attend Offline Consultation',
        'Leave Review and Feedback': 'Leave Review and Feedback'
    }
    return mapping.get(category, 'Other')

df_combined['Touchpoint'] = df_combined['category_keywords'].apply(map_category_to_touchpoint)

touchpoint_counts = df_combined['Touchpoint'].value_counts()
touchpoint_percentages = touchpoint_counts / len(df_combined) * 100

touchpoint_summary = pd.DataFrame({
    'Count': touchpoint_counts,
    'Percentage': touchpoint_percentages
})

def run_root_cause_analysis():
    st.title("Touchpoints Mapping and Root Cause Analysis Dashboard")

    # Load data from CSV
    df_root_causes = pd.read_csv("Root_Cause_Hypothesis/Touchpoints_Final_Sorted.csv")

    # Reorder columns
    column_order = [
        'Touchpoint',
        'Possible Process Issues',
        'Symptoms',
        'Effect of Symptom',
        'Possible Causes',
        'Reasons',
        'Stakeholder'
    ]
    df_root_causes = df_root_causes[column_order]

    st.markdown("""
    This dashboard presents the method for identifying, analyzing, and eliminating issues in the patient lifecycle. 
    It focuses on resolving failures, enhancing process efficiency, and improving patient satisfaction.
    """)

    # Create filters
    col1, col2 = st.columns(2)
    with col1:
        touchpoint = st.multiselect("Touchpoint", options=df_root_causes['Touchpoint'].unique())
    with col2:
        stakeholder = st.multiselect("Process Owner (Stakeholder)", options=df_root_causes['Stakeholder'].unique())

    # Filter data based on selections
    if touchpoint:
        df_root_causes = df_root_causes[df_root_causes['Touchpoint'].isin(touchpoint)]
    if stakeholder:
        df_root_causes = df_root_causes[df_root_causes['Stakeholder'].isin(stakeholder)]

    # Display filtered data
    st.dataframe(df_root_causes)

    # Create visualizations
    st.subheader("Touchpoint Distribution")
    fig = px.pie(df_root_causes, names='Touchpoint', title='Distribution of Touchpoints')
    st.plotly_chart(fig)

    # Stakeholder Distribution
    stakeholder_counts = df_root_causes['Stakeholder'].value_counts().reset_index()
    stakeholder_counts.columns = ['Stakeholder', 'count']
    fig = px.bar(stakeholder_counts, x='Stakeholder', y='count', title='Distribution of Stakeholders')
    st.plotly_chart(fig)

    # Combine with the existing code
    df_part1 = pd.read_csv("Data_Categorization/processed_data_part1.csv")
    df_part2 = pd.read_csv("Data_Categorization/processed_data_part2.csv")
    df_combined = pd.concat([df_part1, df_part2], ignore_index=True)

    # Map categories to touchpoints
    df_combined['Touchpoint'] = df_combined['category_keywords'].apply(map_category_to_touchpoint)

    # Calculate touchpoint statistics
    touchpoint_counts = df_combined['Touchpoint'].value_counts()
    touchpoint_percentages = touchpoint_counts / len(df_combined) * 100

    touchpoint_summary = pd.DataFrame({
        'Count': touchpoint_counts,
        'Percentage': touchpoint_percentages
    })

    st.subheader("Touchpoint Summary from Customer Data")
    st.dataframe(touchpoint_summary)

    # Visualization of touchpoint summary
    fig = px.bar(touchpoint_summary, x=touchpoint_summary.index, y='Percentage', 
                 title='Distribution of Touchpoints from Customer Data')
    st.plotly_chart(fig)

if __name__ == "__main__":
    run_root_cause_analysis()
