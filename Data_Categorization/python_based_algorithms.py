import streamlit as st


def Python_Algorithms():
    st.markdown("""
    <h2 style="color: #00c3a5;">Introduction to Python-Based Algorithms for Feedback Analysis</h2>

    These Python algorithms were developed to efficiently process and analyze large volumes of unstructured user feedback, aiming to uncover key patient concerns. A two-step approach was implemented: the first model focuses on text processing and sentiment analysis to quickly gauge the overall tone, while the second categorizes and extracts touchpoints. This method ensures a structured and precise analysis of the feedback.

    Following this, various graphs, analyses, and trend evaluations will further illustrate the insights derived from the processed data, highlighting patterns and supporting strategic decisions.
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### 1 - Text Processing and Sentiment Analysis
        """)
        with st.expander("See algorithm details"):
            st.write("""
            This algorithm performs comprehensive text processing using **NLTK** (tokenization, lemmatization, and custom stopwords), **VADER** (sentiment analysis), and **Pandas** (data manipulation) to transform and evaluate large volumes of user feedback. It incorporates a custom dictionary of negative words and applies targeted sentiment adjustments, particularly in critical phrases, to accurately identify key issues in user reviews. The algorithm also includes advanced negation handling and performs multidimensional sentiment analysis at the sentence level for more granular evaluation of long texts. Sentiment scores are validated and corrected when necessary to ensure consistency. Additionally, the algorithm leverages **multiprocessing** for parallel processing of data chunks, improving efficiency. Performance is further optimized through caching and just-in-time (JIT) compilation. While effective, this model can be refined to better manage complex language nuances and challenging sentiment cases.
            """)

    with col2:
        st.markdown("""
        ### 2 - Text Categorization and Touchpoint Extraction
        """)
        with st.expander("See algorithm details"):
            st.write("""
            This algorithm leverages **spaCy** (for named entity recognition), **BERT** (for natural language processing, tokenization, and text classification), and **Pandas** (for data manipulation) to automatically categorize user feedback and extract touchpoints. It combines **BERT's** contextual analysis with keyword-based categorization and sentiment adjustment, enhancing the accuracy of classification, especially in critical reviews. The algorithm also includes advanced sentiment manipulation using a custom dictionary of negative phrases, ensuring more precise sentiment interpretation. Additionally, **multiprocessing** is utilized for parallel processing of large datasets, improving efficiency. Performance is further optimized through caching and just-in-time (JIT) compilation. While robust, this model can be refined to better manage complex language nuances and challenging sentiment cases.
            """)

    st.markdown("<hr style='border: 1px solid #00c3a5;'>",
                unsafe_allow_html=True)


# Add this line at the end of the file
__all__ = ['Python_Algorithms']
