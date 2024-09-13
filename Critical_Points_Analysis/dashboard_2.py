from Critical_Points_Analysis.critical_points import critical_points_function  # Certifique-se de que o nome da função está correto
from .mermaid_full_lifecycle import full_lifecycle_sequence_diagram  # Remove the extra 'm'
from .mermaid_compact_lifecycle import compact_lifecycle_sequence_diagram  # Removido o 'm' extra no final
from .touch_points import get_patient_lifecycle  # Importando a função
from .switch_mermaid import toggle_diagram


def run_critical_points_analysis():
    import streamlit as st
    st.title("Critical Points Analysis")
    
    # Chama a função para obter o ciclo de vida do paciente
    get_patient_lifecycle()
    
    # Chama a função para alternar entre os diagramas completo e compacto
    toggle_diagram()
    
    # Chama a função que foi definida no 'critical_points.py'
    critical_points_function()

 