from Critical_Points_Analysis.critical_points import critical_points_function  # Certifique-se de que o nome da função está correto
from .touch_points import get_patient_lifecycle  # Importando a função
from .switch_mermaid import toggle_diagram


import os
import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    file_path_part1 = os.path.join(parent_dir, 'Data_Categorization', 'processed_data_part1.csv')
    file_path_part2 = os.path.join(parent_dir, 'Data_Categorization', 'processed_data_part2.csv')

    if not os.path.exists(file_path_part1) or not os.path.exists(file_path_part2):
        st.error(f"One or both of the required files are missing: {file_path_part1}, {file_path_part2}")
        return None

    df_part1 = pd.read_csv(file_path_part1)
    df_part2 = pd.read_csv(file_path_part2)
    df = pd.concat([df_part1, df_part2], ignore_index=True)
    return df

def run_critical_points_analysis():
    st.title("Critical Points Analysis")
    
    df = load_data()
    if df is None:
        return
    
    # Chama a função para obter o ciclo de vida do paciente
    get_patient_lifecycle()
    
    # Chama a função para alternar entre os diagramas completo e compacto
    toggle_diagram()
    
    # Chama a função que foi definida no 'critical_points.py'
    critical_points_function()


if __name__ == "__main__":
    run_critical_points_analysis()

