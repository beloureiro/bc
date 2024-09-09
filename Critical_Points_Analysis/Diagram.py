import streamlit as st

def display_diagram():
    # Adicione o título e o texto antes da imagem
    st.header("Data Categorization and Analysis Tree")  # Título H2
    st.markdown("""
    --
    Disclaimer: The numbers presented in this conceptual diagram are not real and are used solely for a feasibility study. They are intended to illustrate potential outcomes and should not be interpreted as actual data or predictions.
    """)  # Texto abaixo do título

    # Exibir a imagem
    st.image("Data_Categorization/Data-Categorization-and-Analysis-Tree.png")  # Caminho da imagem

# Adicione esta linha no final do arquivo
__all__ = ['display_diagram']

if __name__ == "__main__":
    display_diagram()
