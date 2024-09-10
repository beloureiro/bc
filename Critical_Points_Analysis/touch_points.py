import streamlit as st

def get_patient_lifecycle():
    content = """
    <h2 style="color: #00c3a5;">Patient Lifecycle within the Care Process: The Journey of Interactions and Experiences Throughout Care</h2>

    ### **Touchpoints**

    In the context of the patient lifecycle within the care process, a touchpoint refers to any interaction the patient has with any part of the process, directly influencing their experience and satisfaction. Complete patient satisfaction is challenging to guarantee because the ownership of touchpoints varies throughout the process. Effective management of this lifecycle often depends on third parties, and despite best efforts, factors such as the quality of medical care—often outside direct control—can significantly impact the patient’s experience.

    Two versions of the process mapping have been developed to support effective management:

    ### **Compact Version**

    The compact version of the process serves as an introduction, focusing on the essential steps to convey the core concept. It simplifies the patient journey, making it easier to grasp the key touchpoints that contribute to patient satisfaction.

    **Identified touchpoints in the process:**

    1. **Search and Schedule Appointment**: The patient interacts with the system to search for and schedule an appointment via Web/App.
    2. **Attend Consultation**: The patient attends the consultation, either online through the platform or in person at the clinic.
    3. **Make Payment**: The patient makes the payment for the consultation, either online through the platform or in person at the reception.
    4. **Leave Review and Feedback**: The patient leaves a review and provides feedback about their overall experience.

    The diagram below illustrates the compact version, highlighting these key touchpoints. This simplified view helps introduce the patient lifecycle concept, emphasizing the importance of each interaction in shaping the overall experience.

    ### **Full Version**

    The full version provides a more detailed and technical perspective, showcasing the complete set of touchpoints that should be managed to ensure optimal patient satisfaction. It covers additional steps, such as online and offline check-ins, accessing the consultation platform, and follow-up procedures.

    **Identified touchpoints in the process:**

    1. **Search and Schedule Appointment**: The patient interacts with the system to search for and schedule an appointment via Web/App.
    2. **Check-in Online**: The patient completes an online check-in before the appointment.
    3. **Check-in at Reception**: The patient checks in at the reception upon arriving at the clinic or hospital.
    4. **Access Platform for Online Consultation**: The patient accesses the online platform to connect with the doctor for the consultation.
    5. **Attend Online Consultation**: The patient attends the online consultation, where the doctor conducts the session through the platform.
    6. **Attend Offline Consultation**: The patient attends an in-person consultation with the doctor at the clinic or hospital.
    7. **Make Payment (Online or at Reception)**: The patient makes the payment for the consultation, either online through the platform or in person at the reception.
    8. **Make Payment at Reception**: The patient makes the payment at the reception after the offline consultation.
    9. **Follow-up Procedures (e.g., Exams, Surgery)**: The patient follows up with any additional procedures, such as exams or surgeries, as prescribed by the doctor.
    10. **Leave Review and Feedback**: The patient leaves a review and provides feedback about their overall experience.

    By clicking the "Show Full Version" button below, the diagram will switch to this more technical view, providing a deeper understanding of the process and illustrating how to effectively manage each touchpoint to improve patient satisfaction.
    """
    
    st.markdown(content, unsafe_allow_html=True)
    st.markdown("<hr style='border: 1px solid #00c3a5;'>", unsafe_allow_html=True)
    

# Adicione esta linha no final do arquivo
__all__ = ['get_patient_lifecycle']
