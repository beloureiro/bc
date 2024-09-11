import streamlit as st

def Python_Algorithms():
    st.markdown("""
    <h2 style="color: #00c3a5;">Introduction to Python-Based Algorithms for Feedback Analysis</h2>

    I developed these Python algorithms to efficiently process and analyze large volumes of unstructured user feedback, aiming to uncover key patient concerns. Given the time constraints, I implemented a two-step approach: the first model focuses on text processing and sentiment analysis to quickly gauge the overall tone, while the second categorizes specific issues and extracts key entities, such as doctor names and locations. This method ensures a structured and precise analysis of the feedback.

    Following this, various graphs, analyses, and trend evaluations will further illustrate the insights derived from the processed data, highlighting patterns and supporting strategic decisions.
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### 1 - Advanced Text Processing and Sentiment Analysis
        """)
        with st.expander("See algorithm details"):
            st.write('''
            This algorithm performs sophisticated text processing using libraries like **NLTK** (tokenization and lemmatization), **VADER** (sentiment analysis), and **Pandas** (data manipulation) to transform and evaluate large volumes of user feedback. It applies a custom dictionary of negative words and dynamically adjusts sentiment polarity, especially in critical phrases, to pinpoint key issues in user reviews. The analysis is enhanced with parallel processing via **multiprocessing** (efficiency), enabling a more detailed assessment of long texts. While efficient, this model can be further refined to better handle complex cases and language nuances that challenge current accuracy levels.
            ''')

    with col2:
        st.markdown("""
        ### 2 - Automated Text Categorization and Entity Extraction
        """)
        with st.expander("See algorithm details"):
            st.write('''
            This algorithm leverages **spaCy** (natural language processing), **BERT** (text classification), and **Pandas** (data manipulation) to automatically categorize user feedback and extract named entities, such as doctor names and locations. By combining specific keywords with BERT classification and utilizing parallel processing via **ThreadPoolExecutor** (efficiency), the algorithm achieves a detailed and customized analysis of each review. While robust, it can be further improved to enhance accuracy, particularly in dealing with complex and nuanced text.
            ''')

    st.markdown("<hr style='border: 1px solid #00c3a5;'>", unsafe_allow_html=True)

# Add this line at the end of the file
__all__ = ['Python_Algorithms']
