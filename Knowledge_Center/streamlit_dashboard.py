# Desabilita todos os avisos
from PIL import Image
import os
import sys
import streamlit as st
import warnings
import base64
from bcframework import run_bcframework
from pathlib import Path

warnings.filterwarnings("ignore")

# Configuração da página (deve ser a primeira chamada)
st.set_page_config(layout="wide", page_title="Business Case Analysis Dashboard")


# Caminho para o diretório do logo
logo_dir = os.path.join(os.getcwd(), 'logo')
logo_path = os.path.join(logo_dir, 'Logo_full.png')

# Verificar se o arquivo existe e exibir na sidebar
if os.path.isfile(logo_path):
    image = Image.open(logo_path)
    resized_image = image.resize((image.size[0] * 2, image.size[1] * 2), Image.LANCZOS)
    st.sidebar.image(resized_image, use_column_width=True)
else:
    st.sidebar.error(f"Logo file not found at {logo_path}")

# Título e separação na barra lateral
st.sidebar.markdown("<h1 style='text-align: center; font-size: 24px;'>Business Case Analysis</h1>", unsafe_allow_html=True)
st.sidebar.markdown("<hr>", unsafe_allow_html=True)

# Barra lateral de navegação
st.sidebar.markdown("<h2 style='text-align: left;'>Navigation</h2>", unsafe_allow_html=True)
page = st.sidebar.radio("Select a Step:", 
                        ("Business Case Framework",
                         "Data Categorization",  # Alterado
                         "Critical Points Analysis",  # Alterado
                         "Root Cause Hypothesis",  # Alterado
                         "Action Plan Development",  # Alterado
                         "Beyond the Scope"),  # Alterado
                        index=0)

# Informações do candidato
st.sidebar.markdown("<hr>", unsafe_allow_html=True)
st.sidebar.markdown("<h5 style='color: rgb(0, 204, 177);'>Candidate:</h5> <h6 style='font-style: italic;'>Bernardo Carvalho</h6>", unsafe_allow_html=True)
st.sidebar.markdown("<h5 style='color: rgb(0, 204, 177);'>Position:</h5> <h6 style='font-style: italic;'>Senior Project Manager - Patient Care</h6>", unsafe_allow_html=True)

# Informações de contato
st.sidebar.markdown("<h5 style='color: rgb(0, 204, 177);'>Contact Information:</h5>", unsafe_allow_html=True)
st.sidebar.markdown("<hr>", unsafe_allow_html=True)

contact_info = [
    ("linkedin.png", "LinkedIn", "bernardoloureiro", "https://www.linkedin.com/in/bernardoloureiro/"),
    ("phone.png", "Phone", "+351 915542701", "tel:+351915542701"),
    ("mail.png", "Email", "bc@inmotion.today", "mailto:bc@inmotion.today"),
    ("globe.png", "Website", "inMotion.today", "https://inmotion.today")
]

for logo, label, value, link in contact_info:
    logo_path = os.path.join(logo_dir, logo)
    if os.path.isfile(logo_path):
        with open(logo_path, "rb") as f:
            logo_data = f.read()
        logo_b64 = base64.b64encode(logo_data).decode()
        st.sidebar.markdown(f"""
            <div style="display: flex; align-items: center; margin-bottom: 10px;">
                <img src="data:image/png;base64,{logo_b64}" alt="{label}" style="width: 20px; height: 20px; margin-right: 10px;">
                <div>
                    <strong>{label}:</strong><br>
                    <a href="{link}" target="_blank" style="color: rgb(0, 204, 177);">{value}</a>
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.sidebar.warning(f"Logo not found: {logo_path}")

# Chamar a função correspondente à página selecionada
if page == "Business Case Framework":
    run_bcframework()
elif page == "Data Categorization":
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from Data_Categorization import dashboard_1
    dashboard_1.run_data_categorization()
elif page == "Critical Points Analysis":
    # Adicione o diretório pai ao sys.path
    current_dir = Path(__file__).resolve().parent
    parent_dir = current_dir.parent
    sys.path.append(str(parent_dir))
    from Critical_Points_Analysis import dashboard_2
    dashboard_2.run_critical_points_analysis()
elif page == "Root Cause Hypothesis":
    # Adicione o diretório pai ao caminho do Python
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.append(parent_dir)
    from Root_Cause_Hypothesis import dashboard_3
    dashboard_3.run_root_cause_hypothesis()
elif page == "Action Plan Development":
    # Get the current file's directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Get the parent directory
    parent_dir = os.path.dirname(current_dir)
    # Add the parent directory to the Python path
    sys.path.append(parent_dir)
    # Now import the run_action_plan_development function
    from Action_Plan_Development.dashboard_4 import run_action_plan_development
    
    # Run the function
    run_action_plan_development()
elif page == "Beyond the Scope":  # Adicione a lógica para a nova página
    from Strategic_Goals import run_strategic_goals
    run_strategic_goals()

# to run the app on gitbash
# source venv/Scripts/activate
# streamlit run Knowledge_Center/streamlit_dashboard.py