import streamlit as st

def run_bcframework():
    st.title("Business Case Framework")
    st.write("Welcome to the Business Case Framework!")
    st.image("logo/bc_framework.png")  # Caminho da imagem
    st.header("Framework Overview")
    st.write("""
    The Business Case Framework consists of four main steps:
    1. Model the Patient Lifecycle and Touchpoints
    2. Develop and Test a Natural Language Processing Algorithm
    3. Prioritize and Breakdown Causes
    4. Develop Actions Based on Identified Causes
    """)
    
   
    # Add more content as needed

if __name__ == "__main__":
    run_bcframework()
