import streamlit as st

def run_bcframework():
    st.title("Business Case Web App")
    st.write("Welcome to the Business Case Web App!")
    st.markdown("""
    This web app was developed to explain the <span style='color: #00c3a5;'><strong>Business Case Framework</strong></span>, which is structured in four stages. 
    The framework begins with mapping the patient lifecycle within the process and identifying critical touchpoints to understand the patient journey. 
    Next, two custom-made Python-based NLP algorithms were developed specifically for this Business Case: the first prepares the data and captures sentiment from user feedback, and the second organizes the cleaned data, correlating the sentiment data with specific processes (touchpoints) to generate a sentiment score for each process based on individual reviews. 
    Following this, the framework uses these sentiment scores to uncover key pain points within the processes. 
    After conducting a root cause analysis and prioritizing the most significant causes, preliminary goals are defined based on internal benchmarks. 
    These goals then guide the development of a strategic action plan aimed at improving patient care, while subtly identifying internal improvement opportunities and potential revenue enhancements.
    """, unsafe_allow_html=True)

    st.write("""
    Below, you will find more detailed information on each of the four stages of the web app.
    """)
    st.image("logo/bc_framework.png")  # Caminho da imagem
    st.write("""
    The process design was prioritized as the fundamental first step for effective data categorization and analysis. Understanding the operation before categorizing ensures a clear relationship between the data and the process.
    By modeling the patient lifecycle and identifying critical touchpoints, data categorization is aligned with operational reality. This structured approach directly connects data to the process's opportunity gaps.
    This integrated view links data analysis with process management, leading to more effective and targeted categorization.
    """)


    st.write("___")  # Linha de separação

    st.markdown("""
    <span style='color: #00c3a5;'><strong>Use the navigation menu on the left (⬅️) to explore each stage of the web app in detail.</strong></span>
    """, unsafe_allow_html=True)



if __name__ == "__main__":
    run_bcframework()
