import streamlit as st
from fase1 import model_patient_lifecycle
from fase2 import develop_nlp_algorithm
from fase3 import prioritize_breakdown_causes
from fase4 import develop_actions


def run_bcframework():
    st.title("Business Case Web App")
    st.write("Welcome to the Business Case Web App!")
    st.write("""
    This web app was developed to explain the Business Case Framework, which is structured in four stages. 
    The framework begins with mapping the patient lifecycle within the process and identifying critical touchpoints to understand the patient journey. 
    Next, a Python-based NLP algorithm is developed and conceptually tested to categorize and analyze user feedback. 
    Following this, the framework correlates sentiment data with specific processes to uncover key pain points. 
    The final objective is to conduct a root cause analysis, leading to the development of a strategic action plan aimed at improving patient care, 
    while subtly identifying internal improvement opportunities and potential revenue enhancements.
    """)
    st.write("""
    Below, you will find more detailed information on each of the four stages of the web app. This will help you understand the processes involved and how each step contributes to the overall goal of improving patient care.
    """)
    st.image("logo/bc_framework.png")  # Caminho da imagem
    st.write("___")  # Linha de separação

    st.write("⚠️ Technical Explanation of the Framework Approach:")
    st.write("""
    The process design was prioritized, establishing the premise that this initial step is fundamental for categorizing and analyzing the data. This approach highlights the importance of understanding the operation before performing categorization, ensuring that the relationship between the data and the process is clear.

    Modeling the patient lifecycle and identifying critical touchpoints allow data categorization to be aligned with operational reality. This perspective organizes the data in a structured way, directly connecting it to the process's opportunity gaps.

    Although the Business Case guidance specifies that the presentation should follow the sequence "Data Categorization," "Pain Point Analysis," "Root Cause Hypothesis," and "Action Plan Development," the process design was prioritized to ensure that all subsequent analyses are conducted in a well-defined context. This way, the established categories are more robust and aligned with the operational flow.

    This approach provides an integrated view, where data analysis is connected to process management, contributing to more effective and targeted categorization.
    """)

    st.write("___")  # Linha de separação
    st.header("Web App Overview")

    st.write(
        "Use the navigation menu on the left (⬅️) to explore each stage of the web app in detail.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("1. Model the Patient Lifecycle and Touchpoints")
        st.write("""
        Mapping the patient lifecycle and identifying critical touchpoints within the process.
        Output: **Touchpoint Mapping & Diagram** – A comprehensive diagram highlighting key touchpoints to optimize patient care.
        """)

        st.subheader(
            "2. Develop and Test a Natural Language Processing Algorithm")
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

    # # Chamada das funções para as quatro etapas
    # model_patient_lifecycle()

    # st.write("___")  # Linha de separação

    # develop_nlp_algorithm()

    # st.write("___")  # Linha de separação

    # prioritize_breakdown_causes()

    # st.write("___")  # Linha de separação

    # develop_actions()


if __name__ == "__main__":
    run_bcframework()
