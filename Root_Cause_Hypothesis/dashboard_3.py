import streamlit as st
from Root_Cause_Hypothesis.Diagram import display_diagram  # Importar a função

def run_root_cause_hypothesis():
    st.title("Root Cause Hypothesis")
    
    # Chama a função para exibir o diagrama
    display_diagram()
    
    # Adicione aqui todo o conteúdo adicional da página de Hipótese de Causa Raiz

# Esta linha garante que a função seja chamada quando o módulo for executado
if __name__ == "__main__":
    run_root_cause_hypothesis()

