from Critical_Points_Analysis.critical_points import critical_points_function  # Certifique-se de que o nome da função está correto
from .mermaid import render_sequence_diagram  # Use o ponto para indicar que está importando do mesmo diretório


def run_critical_points_analysis():
    import streamlit as st
    st.title("Critical Points Analysis")
    
    # Chama a função que foi definida no 'critical_points.py'
    critical_points_function()
    
    # Renderiza o diagrama de sequência
    render_sequence_diagram()  # Chame a função aqui

