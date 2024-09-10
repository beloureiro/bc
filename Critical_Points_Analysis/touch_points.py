import streamlit as st

def get_patient_lifecycle():
    content = """
    <h2 style="color: #00c3a5;">Patient Lifecycle within the Care Process: The Journey of Interactions and Experiences Throughout Care</h2>

    ### **Touchpoints**

    In the context of the patient lifecycle within the care process, a touchpoint refers to any interaction the patient has with any part of the process, directly influencing their experience and satisfaction throughout their care journey. These touchpoints can positively or negatively impact the patient’s experience depending on how they are managed. Therefore, to monitor and optimize patient satisfaction, it is essential to carefully evaluate the experience at each touchpoint.

    **Identified touchpoints in the process:**

    1. **Search and Appointment Scheduling**: The patient interacts with the system to search for and schedule an appointment via Web/App.
    2. **Online Check-in**: The patient completes an online check-in before the appointment.
    3. **Online Consultation (Telemedicine)**: The patient attends the online consultation, connecting with the doctor through the platform.
    4. **Online Payment**: The patient makes the payment for the consultation using the payment platform.
    5. **Review and Feedback**: The patient leaves a review and feedback about the consultation.

    The diagram below illustrates the patient lifecycle within the care process throughout the care journey, highlighting these key touchpoints. Each touchpoint represents a critical opportunity to influence the patient’s experience. While monitoring and optimizing these touchpoints are crucial, they do not necessarily guarantee complete patient satisfaction, as other factors, such as the quality of medical care, also play a crucial role.
    """
    
    st.markdown(content, unsafe_allow_html=True)
    st.markdown("<hr style='border: 1px solid #00c3a5;'>", unsafe_allow_html=True)
    

# Adicione esta linha no final do arquivo
__all__ = ['get_patient_lifecycle']
