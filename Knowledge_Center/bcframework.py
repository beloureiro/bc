import streamlit as st
from fase1 import model_patient_lifecycle
from fase2 import develop_nlp_algorithm
from fase3 import prioritize_breakdown_causes
from fase4 import develop_actions


def run_bcframework():
    st.title("Business Case Web App")
    st.write("Welcome to the Business Case Web App!")
    st.markdown("""
    This web app was developed to explain the <span style='color: #00c3a5;'><strong>Business Case Framework</strong></span>, which is structured in four stages. 
    The framework begins with mapping the patient lifecycle within the process and identifying critical touchpoints to understand the patient journey. 
    Next, a Python-based NLP algorithm is developed and conceptually tested to categorize and analyze user feedback. 
    Following this, the framework correlates sentiment data with specific processes to uncover key pain points. 
    The final objective is to conduct a root cause analysis, leading to the development of a strategic action plan aimed at improving patient care, 
    while subtly identifying internal improvement opportunities and potential revenue enhancements.
    """, unsafe_allow_html=True)
    st.write("""
    Below, you will find more detailed information on each of the four stages of the web app.
    """)
    st.image("logo/bc_framework.png")  # Caminho da imagem
    st.write("___")  # Linha de separação

    st.write("""
    The process design was prioritized, establishing the premise that this initial step is fundamental for categorizing and analyzing the data. This approach highlights the importance of understanding the operation before performing categorization, ensuring that the relationship between the data and the process is clear.

    Modeling the patient lifecycle and identifying critical touchpoints allow data categorization to be aligned with operational reality. This perspective organizes the data in a structured way, directly connecting it to the process's opportunity gaps.

    This approach provides an integrated view, where data analysis is connected to process management, contributing to more effective and targeted categorization.
    """)

    st.write("___")  # Linha de separação

    st.markdown("""
    <span style='color: #00c3a5;'><strong>Use the navigation menu on the left (⬅️) to explore each stage of the web app in detail.</strong></span>
    """, unsafe_allow_html=True)

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
