import streamlit as st
from PIL import Image
import os
import pandas as pd

def load_csv():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, "Smart_Actions_and_Responsibilities.csv")
    
    try:
        df = pd.read_csv(csv_path)
        return df
    except FileNotFoundError:
        st.error(f"Arquivo CSV não encontrado. Verifique se 'Smart_Actions_and_Responsibilities.csv' está em: {csv_path}")
        st.write("Current working directory:", os.getcwd())
        st.write("Contents of current directory:")
        for item in os.listdir(current_dir):
            st.write(f"- {item}")
        return None

def generate_action_plan():
    """
    Generate an action plan based on the given problem statement, goals, and resources.
    """
    st.title("Action Plan")
    
    st.header("Identified Key Issues and Improvement Opportunities:")

    st.markdown("""
    ## ⚠️ Assumption:

    After analyzing the data, stratifying, and prioritizing the causes, the following areas in the process were identified as needing improvement. The causes are listed below, and the points highlighted in the red light are those that demand the most attention for improvements.

    ## Identified Key Issues and Improvement Opportunities:
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("1. Online Consultation:")
        st.markdown("""
        - Poor audio/video quality
        - Difficulty accessing prescriptions
        - Lack of immediate post-consultation support
        - Poor communication between doctor and patient
        - Lack of empathy or attentiveness from the doctor
        """)

        st.subheader("2. Leaving Reviews and Feedback:")
        st.markdown("""
        - Complicated review process
        - Lack of incentives to leave feedback
        - Unclear feedback impact
        """)

        st.subheader("3. Searching and Evaluating Professional Scores:")
        st.markdown("""
        - Inadequate or outdated professional scores
        - Inconsistent or missing reviews
        - Difficult search interface
        """)

    with col2:
        # Tentativa de localizar e exibir a imagem
        possible_paths = [
            "rootcauses.png",
            os.path.join(os.path.dirname(__file__), "rootcauses.png"),
            os.path.join(os.path.dirname(__file__), "..", "rootcauses.png"),
            os.path.join(os.path.dirname(__file__), "..", "Images", "rootcauses.png"),
            r"D:\OneDrive - InMotion - Consulting\DocPlanner\Bc\rootcauses.png"
        ]

        image_found = False
        for path in possible_paths:
            if os.path.exists(path):
                try:
                    image = Image.open(path)
                    st.image(image, caption="Root Causes Analysis", use_column_width=True)
                    image_found = True
                    break
                except Exception as e:
                    st.error(f"Error loading image from {path}: {str(e)}")

        if not image_found:
            st.error("Image not found. Tried the following paths:")
            for path in possible_paths:
                st.write(f"- {path}")
            
            st.write("Current working directory:", os.getcwd())
            st.write("Contents of current directory:")
            for item in os.listdir():
                st.write(f"- {item}")

    display_action_plan_table()

def display_action_plan_table():

    
    df = load_csv()
    if df is not None:
        # Adicionar filtros

        col1, col2, col3 = st.columns(3)
        
        with col1:
            issue = st.multiselect("Identified Issue", options=df["Identified Issue"].unique())
        
        with col2:
            responsible = st.multiselect("Responsible", options=df["Responsible"].unique())
        
        with col3:
            time_bound = st.multiselect("Time-bound", options=df["Time-bound"].unique())
        
        # Aplicar filtros
        if issue:
            df = df[df["Identified Issue"].isin(issue)]
        if responsible:
            df = df[df["Responsible"].isin(responsible)]
        if time_bound:
            df = df[df["Time-bound"].isin(time_bound)]
        
        # Exibir tabela
        st.dataframe(df)

if __name__ == "__main__":
    generate_action_plan()
