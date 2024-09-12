import streamlit as st

def run_bcframework():
    st.title("Business Case Framework")
    st.write("Welcome to the Business Case Framework!")
    st.write("""
    This framework was developed in four stages, beginning with mapping the patient lifecycle within the process and identifying critical touchpoints to understand the patient journey. 
    Next, a Python-based NLP algorithm is developed and conceptually tested to categorize and analyze user feedback. 
    Following this, the framework correlates sentiment data with specific processes to uncover key pain points. 
    The final objective is to conduct a root cause analysis, leading to the development of a strategic action plan aimed at improving patient care, 
    while subtly identifying internal improvement opportunities and potential revenue enhancements.
    """)
    st.image("logo/bc_framework.png")  # Caminho da imagem
    st.header("Framework Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("1. Model the Patient Lifecycle and Touchpoints")
        st.write("""
        Mapping the patient lifecycle and identifying critical touchpoints within the process.
        Output: **Touchpoint Mapping & Diagram** – A comprehensive diagram highlighting key touchpoints to optimize patient care.
        """)
        
        st.subheader("2. Develop and Test a Natural Language Processing Algorithm")
        st.write("""
        A Python-based NLP algorithm is developed and conceptually tested to categorize and analyze patient feedback.
        Output: **Sentiment Analysis** – Detailed sentiment analysis, providing insights into patient emotions.
        """)
    
    with col2:
        st.subheader("3. Prioritize and Breakdown Causes")
        st.write("""
        Correlates the sentiment data with specific processes to identify key pain points in the patient journey.
        Output: **Sentiment-Process Correlation Status** – A status report on the correlation between sentiments and processes, identifying areas for improvement.
        """)
        
        st.subheader("4. Develop Actions Based on Identified Causes")
        st.write("""
        Focuses on conducting a root cause analysis and creating a strategic dashboard.
        Output: **Root Cause Analysis & Dashboard** – Actionable insights and a visual dashboard to drive process improvements and support growth.
        """)
    
    # Add more content as needed

if __name__ == "__main__":
    run_bcframework()
