import streamlit as st

def display_diagram():
    # Adicione o título e o texto antes da imagem
    st.header("Data Categorization and Analysis Tree")  # Título H2
    st.markdown("""
    --
    Disclaimer: The numbers presented in this conceptual diagram are not real and are used solely for a feasibility study. They are intended to illustrate potential outcomes and should not be interpreted as actual data or predictions.
    """)  # Texto abaixo do título

    # Exibir a imagem
    st.image("Data_Categorization/Data-Categorization-and-Analysis-Tree.png")  # Caminho da imagem

    # Adicionar o diagrama de sequência
    st.header("Patient Lifecycle in the Care Process - Sequence Diagram")  # Título H2 para o diagrama de sequência
   
    st.markdown("""
    ```mermaid
    sequenceDiagram
        participant Patient
        participant DocPlanner
        participant InternalSystem
        participant Doctor
        participant Reception

        %% Touchpoint 1: Search and Appointment Scheduling
        Patient->>+DocPlanner: 1. Search and Schedule Appointment
        DocPlanner->>+InternalSystem: Sync Appointment
        InternalSystem-->>+Doctor: Notify Doctor of New Appointment
        InternalSystem-->>-DocPlanner: Confirm Appointment
        DocPlanner-->>-Patient: Confirm Appointment

        %% Touchpoint 2: Online Check-in
        Patient->>+DocPlanner: 2. Check-in Online
        DocPlanner->>+InternalSystem: Update Check-in Data
        InternalSystem-->>-Reception: Notify Check-in

        %% Touchpoint 3: Online Consultation (Telemedicine)
        Patient->>+DocPlanner: 3. Attend Online Consultation
        DocPlanner->>+Doctor: Connect Doctor and Patient
        Doctor-->>-Patient: Conduct Consultation
        Doctor->>+DocPlanner: Add Notes to Patient Record (Consultation Management Tool)
        DocPlanner-->>-Patient: Provide Notes and Prescriptions

        %% Touchpoint 4: Online Payment
        Patient->>+DocPlanner: 4. Make Payment Online
        DocPlanner->>+InternalSystem: Record Payment
        InternalSystem-->>-Reception: Confirm Payment

        %% Touchpoint 5: Review and Feedback
        Patient->>+DocPlanner: 5. Leave Review and Feedback
        DocPlanner->>+DocPlanner: Analyze Patient Feedback

        %% Displaying Reviews and Generating Reports and KPIs (not a touchpoint)
        DocPlanner-->>-OtherPatients: Display Reviews to Help Choose Doctors (independent of medical review)
        DocPlanner->>+Doctor: Generate Reports on Visibility, Reputation, and KPIs
    ```
    """)  # Diagrama de sequência em formato Mermaid
    st.markdown("![](mermaid.py)")  # Inclui o diagrama Mermaid

# Adicione esta linha no final do arquivo
__all__ = ['display_diagram']

if __name__ == "__main__":
    display_diagram()
