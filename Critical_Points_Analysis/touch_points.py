import streamlit as st


def get_patient_lifecycle():
    content = """
    <h3 style="color: #00c3a5;">Touchpoints</h3>

    A touchpoint refers to a specific stage in the process where the patient directly interacts, influencing their experience and satisfaction. Effective management of this lifecycle often depends on third parties, and despite best efforts, factors such as the quality of medical care—often outside direct control—can significantly impact the patient’s experience. In response to these limitations in autonomy, strategic influence actions should be developed to improve sentiment levels and engagement on the platform.


    Two views of the process mapping have been developed to support effective management:
    """

    st.markdown(content, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <span style='color:#00c3a5;'><strong>Compact View</strong></span>  
        The compact view is a simplified, educational version of the process. It focuses on the essential steps, making it easier to understand the key touchpoints that influence patient satisfaction.
        """, unsafe_allow_html=True)

        with st.expander("See identified touchpoints"):
            st.markdown("""
            1. **Search and Schedule Appointment**: The patient interacts with the system to search for and schedule an appointment via Web/App.
            2. **Make Payment**: The patient makes the payment for the consultation, either online through the platform or in person at the reception.
            3. **Attend Consultation**: The patient attends the consultation, either online through the platform or in person at the clinic.
            4. **Leave Review and Feedback**: The patient leaves a review and provides feedback about their overall experience.
            """)

    with col2:
        st.markdown("""
        <span style='color:#00c3a5;'><strong>Full View</strong></span>  
        The full view represents the actual, detailed process, covering all touchpoints that need management for optimal patient satisfaction. It includes additional steps.
        """, unsafe_allow_html=True)

        with st.expander("See identified touchpoints"):
            st.markdown("""
            1. **Search and Evaluate Professional Score**: The patient uses the platform to search for a healthcare professional and evaluate their score.
            2. **Schedule Appointment**: The patient schedules an appointment through the platform.
            3. **Make Payment Online**: The patient makes the payment for the consultation online through the platform.
            4. **Make Payment at Reception**: The patient makes the payment at the reception after the offline consultation.
            5. **Check-in Online**: The patient completes an online check-in before the appointment.
            6. **Check-in at Reception**: The patient checks in at the reception upon arriving at the clinic or hospital.
            7. **Access Platform for Online Consultation**: The patient accesses the online platform to connect with the doctor for the consultation.
            8. **Attend Online Consultation**: The patient attends the online consultation, where the doctor conducts the session through the platform.
            9. **Attend Offline Consultation**: The patient attends an in-person consultation with the doctor at the clinic or hospital.
            10. **Follow-up Procedures (e.g., Exams, Surgery)**: The patient follows up with any additional procedures, such as exams or surgeries, as prescribed by the doctor.
            11. **Leave Review and Feedback**: The patient leaves a review and provides feedback about their overall experience.
            """)

    st.markdown("""
    By clicking the "Show Full View" button below, the diagram will switch to this more technical view, providing a deeper understanding of the process and illustrating how to effectively manage each touchpoint to improve patient satisfaction.
    """)


# Adicione esta linha no final do arquivo
__all__ = ['get_patient_lifecycle']
