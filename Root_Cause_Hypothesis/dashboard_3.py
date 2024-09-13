import streamlit as st
from Root_Cause_Hypothesis.Diagram import display_diagram  # Importar a função
from Root_Cause_Hypothesis.rootdash import root_cause_analysis_panel  # Importar a nova função

def run_root_cause_hypothesis():
    
    # Chama a função do painel de análise de causas raízes
    root_cause_analysis_panel()
    
    # Chama a função para exibir o diagrama
    display_diagram()
    
    
    # Adicione aqui todo o conteúdo adicional da página de Hipótese de Causa Raiz

# Esta linha garante que a função seja chamada quando o módulo for executado
if __name__ == "__main__":
    run_root_cause_hypothesis()

