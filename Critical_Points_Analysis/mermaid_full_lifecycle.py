import streamlit as st  # Certifique-se de que esta linha esteja presente
import streamlit.components.v1 as components  # Importando o componente


def full_lifecycle_sequence_diagram():
    # Adiciona a mensagem antes do diagrama
    st.markdown("<div style='text-align: center;'>⚠️ <strong>Note</strong>: This is the full view of the process. Since there was no opportunity to validate the process steps, there may be some margin for error in modeling this process.</div>", unsafe_allow_html=True)

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
    sequenceDiagram
    participant Patient
    participant DocPlanner
    participant InternalSystem
    participant Doctor
    participant Reception

    %% Touchpoint 1: Search and Evaluate Professional Score
    Patient->>+DocPlanner: 1. Search and Evaluate Professional Score
    DocPlanner-->>-Patient: Display Professional Score

    %% Touchpoint 2: Schedule Appointment
    Patient->>+DocPlanner: 2. Schedule Appointment
    DocPlanner->>+InternalSystem: Sync Appointment
    InternalSystem-->>+Doctor: Notify Doctor of New Appointment
    InternalSystem-->>-DocPlanner: Confirm Appointment
    DocPlanner-->>-Patient: Confirm Appointment

    %% Touchpoint 3: Make Payment (Online or at Reception)
    alt Make Payment Online
        Patient->>+DocPlanner: 3. Make Payment Online
        DocPlanner->>+InternalSystem: Record Payment
        InternalSystem-->>-Reception: Confirm Payment
    else Make Payment at Reception
        Patient->>+Reception: 4. Make Payment at Reception
        Reception->>+InternalSystem: Record Payment
        InternalSystem-->>-DocPlanner: Confirm Payment
    end

    %% Touchpoint 5: Check-in (Online or Offline)
    alt Check-in Online
        Patient->>+DocPlanner: 5. Check-in Online
        DocPlanner->>+InternalSystem: Update Check-in Data
        InternalSystem-->>+Doctor: Notify Doctor of Check-in
    else Check-in at Reception
        Patient->>+Reception: 6. Check-in at Reception
        Reception->>+InternalSystem: Update Patient Arrival
        InternalSystem-->>+Doctor: Notify Doctor of Patient Arrival
    end

    %% Touchpoint 7: Access Platform for Online Consultation
    Patient->>+DocPlanner: 7. Access Platform for Online Consultation
    DocPlanner->>+Doctor: Connect Doctor and Patient

    %% Touchpoint 8: Attend Consultation (Online or Offline)
    alt Online Consultation
        Doctor-->>-Patient: 8. Attend Online Consultation
        Doctor->>+DocPlanner: Add Notes to Patient Record
        DocPlanner-->>-Patient: Provide Notes and Prescriptions
    else Offline Consultation
        Patient->>+Doctor: 9. Attend Offline Consultation
        Doctor-->>-Patient: Conduct In-person Consultation
        Doctor->>+InternalSystem: Add Notes to Patient Record
        InternalSystem-->>-Reception: Provide Notes and Prescriptions
    end

    %% Touchpoint 10: Follow-up Procedures (e.g., Exams, Surgery)
    Patient->>+Doctor: 10. Follow-up Procedures (Doctor Prescribes)
    Doctor-->>+External Providers: Refer Patient for Further Procedures
    External Providers-->>-Patient: Perform Procedures

    %% Touchpoint 11: Leave Review and Feedback
    Patient->>+DocPlanner: 11. Leave Review and Feedback
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
    components.html(html, height=1700, scrolling=False)

    # Exibe o código Mermaid
    # st.code(mermaid_code, language="mermaid")

# Chame a função onde você precisar renderizar o diagrama
