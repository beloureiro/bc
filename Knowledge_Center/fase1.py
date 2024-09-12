import streamlit as st

def model_patient_lifecycle():
    st.subheader("1. Model the Patient Lifecycle and Touchpoints")
    st.write("""
    Mapping the patient lifecycle and identifying critical touchpoints within the process.
    Output: **Touchpoint Mapping & Diagram** – A comprehensive diagram highlighting key touchpoints to optimize patient care.
    """)
    
    # Criando três colunas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Texto na coluna 1
        st.write("""
        **Understanding Patient Touchpoints**

        The Patient Lifecycle within the Care Process encompasses various touchpoints that directly influence a patient's experience and satisfaction. 
        These touchpoints, ranging from scheduling an appointment to providing feedback after a consultation, are critical to ensuring a positive journey. 
        The process can be viewed in two ways: a simplified version that introduces the core steps and a detailed version that includes every interaction point.
        """)


    with col2:
        # Imagem na coluna do meio
        st.image("Knowledge_Center/fase1.png", use_column_width=True)

    with col3:
        # Texto na coluna 3
        st.write("""
        **Managing the Patient Journey**

        Effective management of these touchpoints is essential for optimizing patient satisfaction. 
        The compact version of the process provides an overview of the key interactions, while the full version delves into every detail, ensuring all aspects are considered. 
        To explore these diagrams and understand how each touchpoint contributes to the overall patient experience, click [here].
        """)

