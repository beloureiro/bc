import streamlit as st
import matplotlib.pyplot as plt

def display_text_length_comparison(df):
    st.header('Text Length Comparison')
    col1, col2 = st.columns(2)

    with col1:
        fig1, ax1 = plt.subplots(figsize=(10, 5))
        fig1.patch.set_facecolor('#0e1117')
        ax1.set_facecolor('#262730')
        ax1.clear()
        ax1.boxplot(df['original_length'], patch_artist=True, flierprops=dict(
            markerfacecolor='white', marker='o', markersize=5))
        ax1.set_title('Original Length', color='white')
        ax1.set_ylabel('Length', color='white')
        ax1.tick_params(axis='x', colors='white')
        ax1.tick_params(axis='y', colors='white')

        st.pyplot(fig1, use_container_width=True)

    with col2:
        fig2, ax2 = plt.subplots(figsize=(10, 5))
        fig2.patch.set_facecolor('#0e1117')
        ax2.set_facecolor('#262730')
        ax2.clear()
        ax2.boxplot(df['cleaned_length'], patch_artist=True, flierprops=dict(
            markerfacecolor='white', marker='o', markersize=5))
        ax2.set_title('Cleaned Length', color='white')
        ax2.set_ylabel('Length', color='white')
        ax2.tick_params(axis='x', colors='white')
        ax2.tick_params(axis='y', colors='white')

        st.pyplot(fig2, use_container_width=True)

    mean_original_length = df['original_length'].mean()
    mean_cleaned_length = df['cleaned_length'].mean()
    percent_reduction = (
        (mean_original_length - mean_cleaned_length) / mean_original_length) * 100

    st.write(f"""\
    ### Understanding Text Length Comparison

    This box plot compares the length of the original text to the cleaned text. Here's what it shows:

    1. **Box Plot Elements**:
       - The box represents where 50% of the data falls.
       - The line in the box is the median length.
       - The whiskers show the range of typical lengths.
       - Dots beyond the whiskers are unusual lengths (outliers).

    2. **Key Findings**:
       - Average original text length: {mean_original_length:.0f} characters
       - Average cleaned text length: {mean_cleaned_length:.0f} characters
       - Text reduction: {percent_reduction:.1f}%

    3. **What This Means**:
       - The cleaning process {'significantly' if percent_reduction > 20 else 'moderately' if percent_reduction > 10 else 'slightly'} reduced the text length.
       - {'This suggests a lot of unnecessary content was removed' if percent_reduction > 20 else 'Some unnecessary content was removed, but the core message likely remains intact' if percent_reduction > 10 else 'The cleaning process made minimal changes to the text length'}.

    4. **Why It Matters**:
       - Shorter, cleaner text is often easier to analyze.
       - It helps focus on the most important content.
       - {'The significant reduction might indicate removal of formatting, common words, or repetitive phrases' if percent_reduction > 20 else 'The moderate reduction suggests some refinement without major content loss' if percent_reduction > 10 else 'The minimal reduction indicates the original text was already quite concise'}.
    """)

# Add this line at the end of the file
__all__ = ['display_text_length_comparison']