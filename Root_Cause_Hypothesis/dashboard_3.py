import streamlit as st
from Root_Cause_Hypothesis.Diagram import display_diagram
from Root_Cause_Hypothesis.rootdash import root_cause_analysis_panel
# from Root_Cause_Hypothesis.root_cause import run_root_cause_analysis

def run_root_cause_hypothesis():
    
    st.title("Root Cause Hypothesis Panel")
    # Chama a função do painel de análise de causas raízes
    root_cause_analysis_panel()
    

    # Chama a função run_root_cause_analysis do arquivo root_cause.py
    # run_root_cause_analysis()


    # Chama a função para exibir o diagrama
    display_diagram()

    
    # Adicione aqui todo o conteúdo adicional da página de Hipótese de Causa Raiz

# Esta linha garante que a função seja chamada quando o módulo for executado
if __name__ == "__main__":
    run_root_cause_hypothesis()

