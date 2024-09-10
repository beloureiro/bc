import streamlit as st  # Certifique-se de que esta linha esteja presente
import streamlit.components.v1 as components  # Importando o componente


def render_sequence_diagram():
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
    components.html(html, height=1000, scrolling=False)

    # Exibe o código Mermaid
    # st.code(mermaid_code, language="mermaid")

# Chame a função onde você precisar renderizar o diagrama
