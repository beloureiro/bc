import streamlit as st
import pandas as pd
import sys
import os

# Add the parent directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Now we can import from other modules
from Action_Plan_Development.action_plan import generate_action_plan
from Critical_Points_Analysis.meta_chart import grafico_meta

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

def run_action_plan_development():
    df = load_data()
    if df is None:
        return

    st.title("Action Plan")

    # Chama a função grafico_meta do arquivo meta_chart.py
    grafico_meta(df)  # Passando df como argumento

    generate_action_plan()

if __name__ == "__main__":
    run_action_plan_development()