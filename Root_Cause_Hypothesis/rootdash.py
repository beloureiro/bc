import streamlit as st
import pandas as pd

def root_cause_analysis_panel():
    
    st.markdown(
        "Now that we have identified the <span style='color: #00c3a5;'><strong>prioritized touchpoints</strong></span>, this dashboard serves as a <strong>reference base</strong> for internal brainstorming sessions aimed at validating <span style='color: #00c3a5;'><strong>39</strong></span> potential <span style='color: #00c3a5;'><strong>root causes</strong></span> already mapped within the patient lifecycle. It organizes these causes into specific touchpoints, allowing you to explore the relationships between these touchpoints and stakeholders. The dashboard also features a dynamic table, making it easier to visualize and analyze the data in real-time. By using the filters, you can dive deeper into the data, facilitating discussions on <strong>process inefficiencies</strong> and driving strategies to enhance <strong>performance</strong> and <strong>patient satisfaction</strong>.",
        unsafe_allow_html=True
    )

    st.markdown(
        "Now that the critical points have been identified, select the <strong>critical point - touchpoint</strong> in the filter to navigate through the root causes.",
        unsafe_allow_html=True
    )


    
    st.write("___")  # Linha de separação

    # st.title("Touchpoints Mapping and Root Cause Analysis Dashboard")

    # Load data from CSV
    df = pd.read_csv('Root_Cause_Hypothesis/Touchpoints_Final_Sorted.csv')

    # Reorder columns
    column_order = [
        'Touchpoint',
        'Possible Process Issues',
        'Symptoms',
        'Effect of Symptom',
        'Possible Causes',
        'Reasons',  # This is assumed to be 'Root Causes'
        'Stakeholder'  # This is assumed to be 'Process Owner'
    ]
    df = df[column_order]


    # Create two columns
    col1, col2 = st.columns(2)

    with col2:
        touchpoint = st.multiselect("Touchpoint", options=df['Touchpoint'].unique(), key="touchpoint_rootdash")
        stakeholder = st.multiselect("Process Owner (Stakeholder)", options=df['Stakeholder'].unique(), key="stakeholder_rootdash")
        possible_causes = st.multiselect("Possible Causes", options=df['Possible Causes'].unique(), key="possible_causes_rootdash")

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

        - <span style='color: #00c3a5;'><strong>Touchpoint</strong></span>: The process. <span style='color: #00c3a5'>({len(df['Touchpoint'].unique())})</span>
        - <span style='color: #00c3a5;'><strong>Possible Process Issues</strong></span>: Potential process problems. <span style='color: #00c3a5'>({len(df['Possible Process Issues'].unique())})</span>
        - <span style='color: #00c3a5;'><strong>Symptoms</strong></span>: How the problems are perceived by the patient. <span style='color: #00c3a5'>({len(df['Symptoms'].unique())})</span>
        - <span style='color: #00c3a5;'><strong>Effect of Symptom</strong></span>: Impact of symptoms on the patient experience. <span style='color: #00c3a5'>({len(df['Effect of Symptom'].unique())})</span>
        - <span style='color: #00c3a5;'><strong>Possible Causes</strong></span>: Possible causes of the problems. <span style='color: #00c3a5'>({len(df['Possible Causes'].unique())})</span>
        - <span style='color: #00c3a5;'><strong>Root Causes</strong></span>: Ultimate level factors. <span style='color: #00c3a5'>({len(df['Reasons'].unique())})</span>
        - <span style='color: #00c3a5;'><strong>Process Owner</strong></span>: Oversees the process and drives continuous improvements. <span style='color: #00c3a5'>({len(df['Stakeholder'].unique())})</span>
        """, unsafe_allow_html=True)

    # Rename 'Reasons' column to 'Root Causes' for display purposes
    df_display = df.rename(columns={'Reasons': 'Root Causes'})

    # Data table
    st.dataframe(df_display)

    st.write("___")  # Linha de separação
    
# This line allows the function to be imported in other files
if __name__ == "__main__":
    root_cause_analysis_panel()
