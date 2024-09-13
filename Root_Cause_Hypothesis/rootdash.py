import streamlit as st
import pandas as pd

def root_cause_analysis_panel():
    st.title("Touchpoints Mapping and Root Cause Analysis Dashboard")

    # Load data from CSV
    df = pd.read_csv('Root_Cause_Hypothesis/Touchpoints_Final_Sorted.csv')

    st.markdown("""
    This dashboard is designed to present the method for identifying, analyzing, and eliminating issues in the patient lifecycle. It focuses on definitively resolving failures, enhancing process efficiency, and improving patient satisfaction. The process owner is responsible for implementing the necessary corrections.
    """)

    # Create two columns
    col1, col2 = st.columns(2)

    with col2:
        touchpoint = st.multiselect("Touchpoint", options=df['Touchpoint'].unique())
        stakeholder = st.multiselect("Process Owner (Stakeholder)", options=df['Stakeholder'].unique())
        possible_causes = st.multiselect("Possible Causes", options=df['Possible Causes'].unique())

    # Apply filters
    if touchpoint:
        df = df[df['Touchpoint'].isin(touchpoint)]
    if stakeholder:
        df = df[df['Stakeholder'].isin(stakeholder)]
    if possible_causes:
        df = df[df['Possible Causes'].isin(possible_causes)]

    with col1:
        st.markdown(f"""
        The Structure Consists of the Following Steps:

        - **Touchpoint**: Introduces the process. <span style='color: #00c3a5'>({len(df['Touchpoint'].unique())})</span>
        - **Possible Process Issues**: Potential process problems. <span style='color: #00c3a5'>({len(df['Possible Process Issues'].unique())})</span>
        - **Symptoms**: How the problems are perceived by the patient. <span style='color: #00c3a5'>({len(df['Symptoms'].unique())})</span>
        - **Effect of Symptom**: Impact of symptoms on the patient experience. <span style='color: #00c3a5'>({len(df['Effect of Symptom'].unique())})</span>
        - **Possible Causes**: Possible causes of the problems. <span style='color: #00c3a5'>({len(df['Possible Causes'].unique())})</span>
        - **Root Causes**: Underlying root causes. <span style='color: #00c3a5'>({len(df['Reasons'].unique())})</span>
        - **Process Owner**: Oversees the process and drives continuous improvements. <span style='color: #00c3a5'>({len(df['Stakeholder'].unique())})</span>
        """, unsafe_allow_html=True)

    # Data table
    st.subheader("Root Causes Details")
    st.dataframe(df)

# This line allows the function to be imported in other files
if __name__ == "__main__":
    root_cause_analysis_panel()
