import streamlit as st
import os

def display_news_strategies():
    st.title("AI: Fine-Tuning and Advisory Solutions")
    st.markdown("Below are two advanced AI platforms designed to enhance healthcare: the AI-Powered Healthcare Sentiment Trainer, which fine-tunes models for analyzing patient feedback, and the AI Clinical Advisory Crew framework, which not only provides technical analyses but also serves as a strategic driver for managerial decisions across various operational areas.")

    # Caminho para as imagens
    image_path_1 = os.path.join(os.getcwd(), "logo/rsz_AI_train.png")
    image_path_2 = os.path.join(os.getcwd(), "logo/rsz_cac.png")

    # Criação de duas colunas
    col1, col2 = st.columns(2)

    with col1:
        st.write(f"""
        <span style='color:#3dd56d;'><strong>AI-Powered Healthcare Sentiment Trainer</strong></span> is an advanced platform for fine-tuning AI models like BERT, RoBERTa, and VADER to analyze patient feedback in the healthcare sector, focusing on sentiment analysis tailored to healthcare data.

        **Fine-Tuning Features:**
        - **Healthcare-Specific Sentiment Analysis:** Fine-tunes AI models like BERT, RoBERTa, and VADER to analyze patient feedback with multilingual support.
        - **Adaptable and Updatable Models:** Enables continuous fine-tuning to improve performance as new data is added.
        - **Real-Time Dashboard:** Offers an intuitive interface for input, sentiment results, and performance tracking.
        - **GPU-Enhanced Processing:** Boosts processing speed and efficiency using GPU resources.
        """, unsafe_allow_html=True)
        st.markdown("""
        **Check out the AI-Powered Healthcare Sentiment Trainer on GitHub:** <a href="https://github.com/beloureiro/AI-Powered-Healthcare-Sentiment-Trainer" target="_blank">Visit here</a>.
        """, unsafe_allow_html=True)
        st.image(image_path_1, caption="AI fine-tuning")

    with col2:
        st.write(f"""
        The <span style='color:#3dd56d;'><strong>AI Clinical Advisory Crew</strong></span> is an advanced and flexible system designed to transform the patient experience in healthcare. 
        With a team of specialized AI agents, the project analyzes patient feedback, improves workflows, assesses emotional states, 
        and provides recommendations for operational improvements.
        
        **Key Benefits:**
        - **Improve Patient Experience:** Specialized AI agents analyze feedback, assess emotions, and offer actionable improvements for communication and workflows.
        - **Flexible AI Models:** Dynamically selects the best AI configuration for each task, optimizing performance based on healthcare needs.
        - **Data Security:** Uses local LLMs, ensuring internal data processing and complete privacy without relying on third-party APIs.
        - **Cost Savings:** Eliminates the need for external APIs, reducing operational costs while maintaining high performance and privacy.
        """, unsafe_allow_html=True)

        # Adicionando o link abaixo da lista
        st.markdown("""
        <p><strong>Explore the AI Clinical Advisory Crew Framework:</strong> <a href="https://ai-cac.streamlit.app/">Click here</a> to access the platform.</p>
        """, unsafe_allow_html=True)
        
        st.image(image_path_2, caption="AI Clinical Advisory Crew")

# Esta função pode ser chamada em outra página
