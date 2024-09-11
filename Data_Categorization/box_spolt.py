import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def display_text_length_comparison(df):
    st.header('Text Length Comparison')
    st.markdown("<hr style='border: 1px solid #00c3a5;'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    # Mapeamento dos países
    country_mapping = {
        'br': 'Brazil',
        'de': 'Germany',
        'es': 'Spain',
    }
    available_countries = ['All'] + list(country_mapping.keys())

    with col1:
        selected_country_1 = st.selectbox(
            'Select Country for Original Length',
            available_countries,
            format_func=lambda x: country_mapping.get(x, x)
        )

        # Filtrar dados com base no país selecionado
        filtered_df_1 = df if selected_country_1 == 'All' else df[df['country_code'] == selected_country_1]

        fig1, ax1 = plt.subplots(figsize=(10, 5))
        fig1.patch.set_facecolor('#0e1117')
        ax1.set_facecolor('#262730')
        ax1.clear()
        parts = ax1.violinplot(filtered_df_1['original_length'], showmedians=True, showextrema=True, showmeans=True)
        
        # Alterar a cor da linha da mediana
        median_line = parts['cmedians']
        median_line.set_color('#FF5733')  # Cor laranja para destaque
        
        # Alterar a cor do corpo do gráfico
        for pc in parts['bodies']:
            pc.set_facecolor('#1f77b4')
            pc.set_edgecolor('white')
            pc.set_alpha(0.75)
        
        ax1.set_title('Original Length', color='white')
        ax1.set_ylabel('Length (characters)', color='white')
        ax1.tick_params(axis='x', colors='white')
        ax1.tick_params(axis='y', colors='white')

        st.pyplot(fig1, use_container_width=True)

        # Texto explicativo para o gráfico de comprimento original
        mean_original_length = filtered_df_1['original_length'].mean()

        st.write(f"""
        ### Understanding Text Length Comparison

        This violin plot compares the length of the original text across different samples. Here's what it shows:

        1. **Violin Plot Elements**:
           - The **shape** represents the distribution of the data across different lengths.
           - The **orange line** in the middle is the **median length**.
           - The **lines within the plot** indicate the quartiles (25th, 50th, 75th percentiles), and the **outermost lines** show the range of the data (excluding outliers).
           - The **width** of the plot at different points represents the **density** of the data: wider sections indicate more frequent lengths, while narrower sections indicate less frequent lengths.

        2. **Key Finding**:
           - **Original Text** ({country_mapping.get(selected_country_1, 'All Countries')}): Average length is {mean_original_length:.0f} characters.
        """)

    with col2:
        selected_country_2 = st.selectbox(
            'Select Country for Cleaned Length',
            available_countries,
            format_func=lambda x: country_mapping.get(x, x)
        )

        # Filtrar dados com base no país selecionado
        filtered_df_2 = df if selected_country_2 == 'All' else df[df['country_code'] == selected_country_2]

        fig2, ax2 = plt.subplots(figsize=(10, 5))
        fig2.patch.set_facecolor('#0e1117')
        ax2.set_facecolor('#262730')
        ax2.clear()
        parts = ax2.violinplot(filtered_df_2['cleaned_length'], showmedians=True, showextrema=True, showmeans=True)
        
        # Alterar a cor da linha da mediana
        median_line = parts['cmedians']
        median_line.set_color('#FF5733')  # Cor laranja para destaque
        
        # Alterar a cor do corpo do gráfico
        for pc in parts['bodies']:
            pc.set_facecolor('#00c3a5')
            pc.set_edgecolor('white')
            pc.set_alpha(0.75)
        
        ax2.set_title('Cleaned Length', color='white')
        ax2.set_ylabel('Length (characters)', color='white')
        ax2.tick_params(axis='x', colors='white')
        ax2.tick_params(axis='y', colors='white')

        st.pyplot(fig2, use_container_width=True)

        # Cálculos adicionais e explicação para o gráfico de comprimento limpo
        mean_cleaned_length = filtered_df_2['cleaned_length'].mean()
        percent_reduction = ((mean_original_length - mean_cleaned_length) / mean_original_length) * 100

        st.write(f"""
        3. **Text Reduction**:
           - **Cleaned Text** ({country_mapping.get(selected_country_2, 'All Countries')}): Average length is {mean_cleaned_length:.0f} characters.
           - **Reduction**: There is a {percent_reduction:.1f}% reduction in text length after cleaning.

        4. **What This Means**:
           - The cleaning process {'significantly' if percent_reduction > 20 else 'moderately' if percent_reduction > 10 else 'slightly'} reduced the text length.
           - {'This suggests that a significant amount of unnecessary content, such as filler words or formatting, was removed, improving clarity and focus.' if percent_reduction > 20 else 'The moderate reduction indicates that the cleaning process refined the text without removing too much valuable content.' if percent_reduction > 10 else 'The minimal reduction suggests that the original text was already concise and well-formatted.'}

        5. **Why It Matters**:
           - **Cleaner Text**: Shorter, cleaner text is easier to analyze and interpret.
           - **Focus on Content**: The reduction highlights the removal of superfluous content, which helps focus on the core message.
           - **Impact on Analysis**: The changes in text length can affect subsequent analyses, such as sentiment analysis or keyword extraction, by improving the signal-to-noise ratio.
        """)

# Add this line at the end of the file
__all__ = ['display_text_length_comparison']
