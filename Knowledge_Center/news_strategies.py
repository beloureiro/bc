import streamlit as st
import os

def display_news_strategies():
    # Obter o caminho absoluto para a pasta de assets
    current_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(current_dir, 'assets')

    st.title("Key Strategic Initiatives")

    # Criando as 5 abas com o nome atualizado para a primeira
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "New Value Proposition",
        "Enhanced Review System",
        "Current Review System",
        "Growth & Mentorship Ecosystem",
        "24/7 AI-Skills Advisor"
    ])

    # Conteúdo da primeira aba (New Value Proposition)
    with tab1:

        # Título da Análise
        st.markdown("<h2 style='color: #00c3a5;'>Analysis of the New Value Proposition</h2>", unsafe_allow_html=True)

        # Exibindo a Proposta de Valor Atualizada
        st.markdown("The New Value Proposition is:")
        st.markdown("""
        <div style='background-color: #262730; border-radius: 10px; padding: 20px; text-align: center; font-size: 24px;'>
            <strong>Patient get to know you <span style='color: #00c3a5; font-size: 26px;'>+</span> Patients get to trust you <span style='color: #00c3a5; font-size: 26px;'>=</span> Patients get to book with you <span style='color: #00c3a5; font-size: 26px;'>+</span> Patients' expectations are met <span style='color: #00c3a5; font-size: 26px;'>=</span> Patients become loyal and recommend you to others</strong>
        </div>
        """, unsafe_allow_html=True)

        # Abordando os problemas da proposta de valor anterior
        st.markdown("""
        **How the New Value Proposition Addresses Previous Issues:**

        - **Expanded Focus Beyond Booking:** The New Value Proposition goes beyond the booking phase. It emphasizes that meeting patients' expectations is crucial for fostering loyalty and recommendation.

        - **Expectation Management and Quality Assurance:** By focusing on meeting patient expectations, it helps ensure that patients receive the level of care they anticipate, reducing dissatisfaction and aligning with the services provided.

        - **Post-Consultation Support and Loyalty Building:** The New Value Proposition highlights that fulfilling expectations naturally leads to loyalty and recommendations, encouraging a long-term relationship with patients.
        """)


    # Conteúdo das outras abas (vazias por enquanto)
    with tab2:
        st.write("### Enhanced Review System")

        col1, col2 = st.columns(2)

        with col1:
            image_path = os.path.join(assets_dir, 'Revew_app1.png')
            try:
                st.image(image_path, use_column_width=True, caption="Review App - Professional List")
            except Exception as e:
                st.error(f"Error loading image: {image_path}. Error: {str(e)}")
        
        with col2:
            image_path = os.path.join(assets_dir, 'Revew_app2.png')
            try:
                st.image(image_path, use_column_width=True, caption="Review App - Detailed Ratings")
            except Exception as e:
                st.error(f"Error loading image: {image_path}. Error: {str(e)}")

        st.write("""
        The Enhanced Review System offers patients a structured and insightful way to assess healthcare professionals. Through this updated system, patients benefit from a more organized categorization of review criteria and detailed professional profiles. Key benefits include:

        1. **Structured Review System**: Patients can rate multiple aspects of their care experience, including waiting time, communication quality, value perception, and support staff attentiveness. This structured approach provides a more comprehensive and balanced view of the professional's care quality.
        2. **Detailed Profile View**: Each professional's profile includes an overall rating, availability, and in-depth ratings on specific aspects of care. The "Style of Care" section visually represents the doctor's approach, helping patients choose a provider that aligns with their expectations and personal preferences.
        3. **Patient Feedback Survey**: The interactive feedback survey allows patients to provide nuanced feedback on various care aspects. Patients rate experiences using a sliding scale, covering areas like environment satisfaction and interaction style, thereby enabling a tailored care alignment that benefits future patients.
        4. **Enhanced Patient Insights**: The categorized feedback enables patients to make well-informed choices based on detailed reviews, reducing uncertainty and promoting confidence before scheduling an appointment.
        5. **Transparency and Trust**: This system fosters transparency by showcasing authentic feedback, allowing healthcare providers to align their service with patient expectations effectively.

        Overall, this app enhances the decision-making process for both patients and healthcare providers by offering a clearer view of care experiences and aligning patient needs with professional care styles. 

        You can access the published version of the app here: [Care Review App](https://beloureiro.github.io/carereview/)
        """)


    with tab3:
        st.write("### Current Review System")
        
        st.write("""
        The current review system allows patients to provide feedback on their healthcare experiences. This system has some limitations compared to more advanced review systems.

        Key points about the current review system:
        1. Simple star rating: Patients can rate their overall experience using a 5-star scale.
        2. Text-based feedback: There's an option for patients to leave written comments about their experience.
        3. Limited categorization: The system doesn't break down ratings into specific aspects of care.
        4. Basic display: The interface shows an average rating and individual reviews without detailed analytics.

        While this system provides valuable feedback, it has potential for improvement to offer more detailed insights and a better user experience for both patients and healthcare providers.
        """)

        image_path = os.path.join(assets_dir, 'Current_review.png')
        try:
            st.image(image_path, use_column_width=True, caption="Current Review System")
        except Exception as e:
            st.error(f"Error loading image: {image_path}. Error: {str(e)}")
        
        st.write("""
        The image above illustrates our current review system. This system allows patients to provide feedback on their healthcare experiences, but it has some limitations compared to the enhanced review system we're developing.

        Key points about the current review system:
        1. Simple star rating: Patients can rate their overall experience using a 5-star scale.
        2. Text-based feedback: There's an option for patients to leave written comments about their experience.
        3. Limited categorization: The current system doesn't break down ratings into specific aspects of care.
        4. Basic display: The interface shows an average rating and individual reviews without detailed analytics.

        While this system provides valuable feedback, we're working on enhancing it to offer more detailed insights and a better user experience for both patients and healthcare providers.
        """)

    with tab4:
        st.write("### Growth & Mentorship Ecosystem")

        col1, col2 = st.columns(2)

        with col1:
            image_path = os.path.join(assets_dir, 'AIcrew.png')
            try:
                st.image(image_path, use_column_width=True, caption="AI Crew Overview")
            except Exception as e:
                st.error(f"Error loading image: {image_path}. Error: {str(e)}")

        with col2:
            image_path = os.path.join(assets_dir, 'AIcrew2.png')
            try:
                st.image(image_path, use_column_width=True, caption="AI Crew Detailed View")
            except Exception as e:
                st.error(f"Error loading image: {image_path}. Error: {str(e)}")

        st.write("""
        The Growth & Mentorship Ecosystem is designed to support healthcare professionals in their continuous development and improvement. This system leverages AI and data-driven insights to provide personalized guidance and mentorship opportunities.

        Key features of the ecosystem include:
        1. Personalized learning paths based on individual strengths and areas for improvement
        2. AI-powered mentorship matching, connecting professionals with experienced mentors in their field
        3. Real-time feedback and performance analytics to track progress
        4. Collaborative learning opportunities through virtual peer groups
        5. Access to a vast knowledge base of best practices and latest medical research

        This ecosystem aims to foster a culture of continuous improvement and excellence in healthcare delivery, ultimately benefiting both healthcare professionals and their patients.
        """)
        st.markdown("""
                <p><strong>Explore the AI Clinical Advisory Crew Framework:</strong> <a href="https://ai-cac.streamlit.app/">Click here</a> to access the platform.</p>
            """, unsafe_allow_html=True)

    with tab5:
        st.write("### 24/7 Chatbot")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("""
            The AI-Skills Advisor is a key component of the AI Clinical Advisory Crew. It provides continuous, data-driven support to healthcare professionals. The advisor offers the following capabilities:

            1. Analyze patient feedback and generate insights to improve care quality.
            2. Identify opportunities to enhance workflows and processes in healthcare delivery.
            3. Offer communication strategies to improve patient-provider interactions.
            4. Provide psychological insights for better post-consultation patient care.
            5. Deliver managerial overviews and summaries of patient feedback.
            6. Offer personalized recommendations for professional development.
            7. Provide instant, 24/7 access to AI-driven guidance and support.

            This tool aims to help healthcare professionals excel in their practice by leveraging AI-powered insights and continuous learning.
            """)
        with col2:
            st.markdown("""
                <p><strong>Explore the AI Clinical Advisory Crew Framework:</strong> <a href="https://ai-cac.streamlit.app/">Click here</a> to access the platform.</p>
            """, unsafe_allow_html=True)

            image_path = os.path.join(assets_dir, 'bot.png')
            try:
                st.image(image_path, use_column_width=True, caption="AI-Skills Advisor Interface")
            except Exception as e:
                st.error(f"Error loading image: {image_path}. Error: {str(e)}")
