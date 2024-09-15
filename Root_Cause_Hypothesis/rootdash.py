import streamlit as st
import pandas as pd

def root_cause_analysis_panel():
    
    st.markdown(
    "Now that we have identified the <span style='color: #00c3a5;'><strong>prioritized touchpoints</strong></span>, this tool serves as a <strong>reference base</strong> for internal brainstorming sessions aimed at validating <span style='color: #00c3a5;'><strong>39</strong></span> potential <span style='color: #00c3a5;'><strong>root causes</strong></span> that have already been mapped across the 11 touchpoints of the process. It organizes these causes into specific touchpoints, allowing you to explore the relationships between these touchpoints and stakeholders. By using a dynamic table, it makes it easier to visualize and analyze all the possible root causes.",
    unsafe_allow_html=True
    )

    st.markdown("""
    ➡️**Instructions:**
    The panel is currently filtered to the top priority touchpoints identified in the previous session, which together account for approximately <span style='color:#00c3a5;'>90% </span><span style='color:#ffffff;'>of the</span><span style='color:#00c3a5;'> root causes</span>:

    - <span style='color:#00c3a5;'><strong>1 - Attend Online Consultation</strong></span> (62.3%)
    - <span style='color:#00c3a5;'><strong>2 - Leave Review and Feedback</strong></span> (25.08%)
    - <span style='color:#00c3a5;'><strong>3 - Search and Evaluate Professional Score</strong></span> (1.65%)

    *Note: The "Search and Evaluate Professional Score" touchpoint represents a strategic action designed to exert influence and improve overall engagement on the platform.*

    These were flagged as the most critical areas. To explore different root causes, simply adjust the filters below.
    """, unsafe_allow_html=True)



    
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
        default_touchpoints = [
            "Attend Online Consultation",
            "Leave Review and Feedback",
            "Search and Evaluate Professional Score"
        ]
        touchpoint = st.multiselect(
            "Touchpoint", 
            options=df['Touchpoint'].unique(), 
            default=default_touchpoints,
            key="touchpoint_rootdash"
        )
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
