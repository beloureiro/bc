import streamlit as st

def display_diagram():
    # Adicione o título e o texto antes da imagem
    st.markdown("""
    ⚠️ Note: The numbers in this diagram are illustrative. They demonstrate how stratification effectively identifies opportunities.
    """)  # Texto abaixo do título

    # Exibir a imagem
    st.image("Root_Cause_Hypothesis/Data-Categorization-and-Analysis-Tree.png")  # Caminho da imagem

# Adicione esta linha no final do arquivo
__all__ = ['display_diagram']

if __name__ == "__main__":
    display_diagram()
