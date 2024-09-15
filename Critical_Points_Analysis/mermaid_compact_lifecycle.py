import streamlit as st  # Certifique-se de que esta linha esteja presente
import streamlit.components.v1 as components  # Importando o componente


def compact_lifecycle_sequence_diagram():
    # Adiciona a mensagem antes do diagrama
    st.markdown("<div style='text-align: center;'>⚠️ <strong>Note</strong>: This is the compact view of the process. Since there was no opportunity to validate the process steps, there may be some margin for error in modeling this process.</div>", unsafe_allow_html=True)

    # Código Mermaid
    mermaid_code = """
    %%{init: {
        'theme': 'dark',
        'themeVariables': {
            'actorTextColor': '#FFFFFF',
            'actorLineColor': '#00c3a5',
            'signalColor': '#00c3a5',
            'signalTextColor': '#FFFFFF',
            'labelTextColor': '#FFFFFF',
            'noteBkgColor': '#262730',
            'noteTextColor': '#FFFFFF'
        }
    }}%%
    %%height 100%
    sequenceDiagram
    participant Patient
    participant DocPlanner
    participant Doctor
    participant OtherPatients

    %% Touchpoint 1: Search and Schedule Appointment
    Patient->>+DocPlanner: 1. Search and Schedule Appointment
    DocPlanner->>+Doctor: Notify Doctor of New Appointment
    DocPlanner-->>-Patient: Confirm Appointment

    %% Touchpoint 2: Make Payment
    Patient->>+DocPlanner: 2. Make Payment
    DocPlanner-->>-Patient: Confirm Payment

    %% Touchpoint 3: Attend Consultation
    Patient->>+DocPlanner: 3. Attend Consultation
    DocPlanner->>+Doctor: Connect Doctor and Patient (Online) / Notify Doctor of Arrival (Offline)
    Doctor-->>-Patient: Conduct Consultation
    Doctor->>+DocPlanner: Add Notes to Patient Record
    DocPlanner-->>-Patient: Provide Notes and Prescriptions

    %% Touchpoint 4: Leave Review and Feedback
    Patient->>+DocPlanner: 4. Leave Review and Feedback
    DocPlanner->>+Doctor: Share Feedback
    DocPlanner-->>-OtherPatients: Display Reviews to Help Choose Doctors



    """

    # HTML com o script Mermaid e o diagrama
    html = f"""
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script>
        mermaid.initialize({{
            startOnLoad: true,
            theme: 'dark',
            securityLevel: 'loose',
            fontFamily: 'Arial',
        }});
    </script>
    <div class="mermaid" style="height:100vh;">
    {mermaid_code}
    </div>
    """

    # Renderiza o HTML
    components.html(html, height=900, scrolling=False)

    # Exibe o código Mermaid
    # st.code(mermaid_code, language="mermaid")

# Chame a função onde você precisar renderizar o diagrama
