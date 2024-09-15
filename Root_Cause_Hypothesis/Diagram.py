import streamlit as st

def display_diagram():
    # Adicione o título e o texto antes da imagem
    st.markdown("""
    ⚠️ Note: The numbers in this diagram are illustrative. This example demonstrates how a tree view can be a useful tool for identifying opportunities through stratification. The practical application of this approach depends on having more data, which is currently unavailable in this business case database. However, this does not limit the demonstration of the methodology and the ability to apply it effectively.
    """)

    

    # Exibir a imagem
    st.image("Root_Cause_Hypothesis/Data-Categorization-and-Analysis-Tree.png")  # Caminho da imagem

# Adicione esta linha no final do arquivo
__all__ = ['display_diagram']

if __name__ == "__main__":
    display_diagram()
