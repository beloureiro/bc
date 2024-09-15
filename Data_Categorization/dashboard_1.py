import streamlit as st  # Importando streamlit corretamente no início
import io as original_io
import base64
import io
import sys
import warnings
from collections import Counter
import os  # Adicionando a importação do módulo os

import matplotlib.colors as mcolors
import matplotlib.dates as mdates
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image
from wordcloud import WordCloud

import numpy as np
import pandas as pd


from Data_Categorization.python_based_algorithms import Python_Algorithms  # Add this import
from Data_Categorization.box_spolt import display_text_length_comparison
from Data_Categorization.Categorized_data import display_categorized_data

warnings.filterwarnings("ignore")

# Save the original io module
# Import numpy, which might overwrite io
# Restore the original io module
sys.modules['io'] = original_io

# Função para contar palavras


def count_words(text):
    words = text.split()
    return Counter(words)

# Função para gerar a nuvem de palavras com fundo escuro


def generate_wordcloud(word_freq, title, filtered_df):
    wordcloud = WordCloud(width=800, height=400, background_color='#262730',
                          colormap='viridis').generate_from_frequencies(word_freq)

    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor('#0e1117')  # Cor de fundo da figura
    ax.set_facecolor('#262730')  # Cor de fundo do eixo

    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    ax.set_title(title, color='white')

    img = io.BytesIO()
    plt.savefig(img, format='PNG', facecolor='#0e1117', edgecolor='none')
    img.seek(0)
    plt.close()
    return base64.b64encode(img.getvalue()).decode()

# Função para auditar os dados


def audit_data(word_freq, common_words_df):
    df_words = set(common_words_df['Word'])
    freq_words = set(word_freq.keys())

    if not df_words.issubset(freq_words):
        missing_words = df_words - freq_words
        return f"Inconsistency detected. Words in table but not in frequency data: {', '.join(missing_words)}"

    for _, row in common_words_df.iterrows():
        if word_freq[row['Word']] != row['Count']:
            return f"Inconsistency detected. Count mismatch for word '{row['Word']}'"

    return "Data is consistent between word frequency and table."

# Crie a função run_data_categorization que encapsula todo o conteúdo principal


def run_data_categorization():
    # Load data (keep your existing code for loading data)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path_part1 = os.path.join(current_dir, 'processed_data_part1.csv')
    file_path_part2 = os.path.join(current_dir, 'processed_data_part2.csv')

    if not os.path.exists(file_path_part1) or not os.path.exists(file_path_part2):
        st.error(f"One or both of the required files are missing: {
                 file_path_part1}, {file_path_part2}")
        st.stop()

    df_part1 = pd.read_csv(file_path_part1, encoding='utf-8')
    df_part2 = pd.read_csv(file_path_part2, encoding='utf-8')
    df = pd.concat([df_part1, df_part2], ignore_index=True)

    df['created_at'] = pd.to_datetime(df['created_at'])
    df['year_week'] = df['created_at'].dt.to_period('W')

    # Add sidebar filters
    st.sidebar.header('Filters')

    # Country filter
    country_mapping = {
        'br': 'Brazil',
        'de': 'Germany',
        'es': 'Spain',
    }
    available_countries = ['All'] + list(country_mapping.keys())
    selected_country = st.sidebar.selectbox(
        'Select Country', available_countries, format_func=lambda x: country_mapping.get(x, x))

    # Feedback type filter
    available_types = ['All'] + list(df['type'].unique())
    selected_type = st.sidebar.selectbox(
        'Select Feedback Type', available_types)

    # Week filter
    available_weeks = ['All'] + \
        list(df['year_week'].dt.strftime('%Y-W%W').unique())
    selected_week = st.sidebar.selectbox('Select Week', available_weeks)

    # Apply filters
    filtered_df = df.copy()
    if selected_country != 'All':
        filtered_df = filtered_df[filtered_df['country_code']
                                  == selected_country]
    if selected_type != 'All':
        filtered_df = filtered_df[filtered_df['type'] == selected_type]
    if selected_week != 'All':
        filtered_df = filtered_df[filtered_df['year_week'].dt.strftime(
            '%Y-W%W') == selected_week]

    # Título principal
    st.title('Data Processing, Analysis, and Categorization')

    # st.markdown("<h3 style='color: #00c3a5;'>This section covers the ETL process for text analysis and sentiment evaluation.</h3>", unsafe_allow_html=True)

    # Add the Python_Algorithms content here
    Python_Algorithms()

    st.write(
        "Note: The table above displays only the first 5 rows from the full dataset.")

    # Dicionário para mapear tipos
    type_mapping = {
        'case': 'Case',
        'opinion': 'Opinion',
        'csat': 'Customer Satisfaction (CSAT)',
        'promoter ninja': 'Promoter Ninja',
        'appfollow': 'AppFollow',
    }

    # Dicionário para mapear países
    country_mapping = {
        'br': 'Brazil',
        'de': 'Germany',
        'es': 'Spain',
    }

    # Definir country_options
    country_options = ['All'] + list(country_mapping.values())

    # Display the first few rows of the filtered dataframe
    st.write(filtered_df.head())

    # Temporal Analysis
    st.header('Temporal Analysis')
    st.markdown("<hr style='border: 1px solid #00c3a5;'>",
                unsafe_allow_html=True)
    st.write("""
    This section presents a temporal analysis based on the dataset spanning from April 1st, 2024, to June 30th, 2024, covering a total duration of 91 days. The dataset is organized into 13 weeks. Within this period, the analysis includes data from three countries: Spain (es), Germany (de), and Brazil (br), with a total of 44,851 records.
    """)

    # Preparar dados
    weekly_counts = filtered_df.groupby('year_week').size()
    sentiment_counts = filtered_df.groupby('year_week')['original_sentiment'].agg([
        'mean', 'count']).reset_index()
    country_time_distribution = filtered_df.groupby(
        ['year_week', 'country_code']).size().unstack(fill_value=0)
    country_time_distribution_percentage = country_time_distribution.div(
        country_time_distribution.sum(axis=1), axis=0)

    # Criar duas linhas com duas colunas cada para os gráficos
    row1_col1, row1_col2 = st.columns(2)
    row2_col1, row2_col2 = st.columns(2)

    with row1_col1:
        # Filtro de país para o gráfico de contagem de registros
        selected_country_1 = st.selectbox(
            'Select Country for Record Count', available_countries, format_func=lambda x: country_mapping.get(x, x))

        # Filtrar o DataFrame original com base no país selecionado
        filtered_df_1 = filtered_df.copy()
        if selected_country_1 != 'All':
            filtered_df_1 = filtered_df_1[filtered_df_1['country_code'] == selected_country_1]

        filtered_weekly_counts = filtered_df_1.groupby('year_week').size().reset_index(name='count')
        filtered_weekly_counts['week_number'] = filtered_weekly_counts['year_week'].dt.week

        # Check if filtered_weekly_counts is empty
        if filtered_weekly_counts.empty:
            st.warning(
                "No data available for the selected combination of country and feedback type.")
        else:
            # Cálculo das variáveis para interpretação
            mean_value = filtered_weekly_counts['count'].mean()
            std_dev = filtered_weekly_counts['count'].std()
            cv = (std_dev / mean_value) * 100 if mean_value != 0 else 0

            # Interpretação do CV
            if cv < 10:
                cv_interpretation = "a low variability around the mean, suggesting high stability in weekly record counts."
                cv_level = "lower"
                stability_level = "stable and consistent"
                cv_comparison = "lower"
                fluctuation_description = "minor fluctuations"
            elif 10 <= cv <= 20:
                cv_interpretation = "a moderate level of variability, which indicates the possibility of occasional fluctuations in weekly record counts."
                cv_level = "moderate"
                stability_level = "less stable and consistent"
                cv_comparison = "higher"
                fluctuation_description = "more significant fluctuations"
            else:
                cv_interpretation = "a high level of variability, suggesting that weekly record counts experience significant fluctuations, potentially requiring further investigation to identify underlying causes."
                cv_level = "higher"
                stability_level = "less stable and consistent"
                cv_comparison = "higher"
                fluctuation_description = "more significant fluctuations"

            # Cálculo da tendência
            z = np.polyfit(
                filtered_weekly_counts['week_number'], filtered_weekly_counts['count'], 1)
            slope = z[0]
            trend_direction = "increases" if slope > 0 else "decreases"
            slope_value_absolute = abs(slope)
            trend_type = "positive" if slope > 0 else "negative"
            trend_direction_word = "upward" if slope > 0 else "downward"
            trend_implication = (
                "more records are being collected, indicating a possible increase in data submissions over time"
                if slope > 0
                else "fewer records are being collected, which could suggest a decline in data submissions over time"
            )

            # Gráfico de contagem de registros por semana
            fig1, ax1 = plt.subplots(figsize=(10, 6))
            fig1.patch.set_facecolor('#0e1117')
            ax1.set_facecolor('#262730')
            bars = ax1.bar(filtered_weekly_counts['week_number'],
                           filtered_weekly_counts['count'], color='#00C3A5', label='Record Count')

            # Adicionar a linha da média
            ax1.axhline(mean_value, color='blue', linestyle='-', label=f'Average: {
                        mean_value:.0f} (Coefficient of Variation: {cv:.2f}%)')

            # Calcular a linha de tendência
            p = np.poly1d(z)
            ax1.plot(filtered_weekly_counts['week_number'], p(
                filtered_weekly_counts['week_number']), "r--", label=f'Trend (Slope: {z[0]:.2f})')

            # Configurar o eixo X para mostrar todas as 13 semanas
            all_weeks = range(filtered_weekly_counts['week_number'].min(
            ), filtered_weekly_counts['week_number'].max() + 1)
            ax1.set_xticks(all_weeks)
            ax1.set_xticklabels(all_weeks, rotation=45, ha='right')

            ax1.set_title('Record Count per Week', color='white')
            ax1.set_xlabel('Week Number', color='white')
            ax1.set_ylabel('Number of Records', color='white')
            ax1.tick_params(axis='x', colors='white')
            ax1.tick_params(axis='y', colors='white')
            legend1 = ax1.legend(facecolor='black', edgecolor='white')
            for text in legend1.get_texts():
                text.set_color('white')
            plt.tight_layout()
            st.pyplot(fig1, use_container_width=True)

            st.write("### Interpreting Record Count per Week")

            st.write(
                "This graph illustrates the number of records collected each week:")

            with st.expander("See explanation"):

                st.write(f"""
                1. **Average Line**: The blue solid line represents the average number of records per week, which is **{mean_value:.0f}**. The coefficient of variation (CV) is **{cv:.2f}**%, indicating **{cv_interpretation}**. A **{cv_level}** CV suggests **{stability_level}** in weekly record counts, with **{fluctuation_description}**.
                2. **Trend**: The red dashed line represents the overall trend in record counts over time. The slope of this line is **{slope:.2f}**, meaning that, on average, the number of records **{trend_direction}** by approximately **{slope_value_absolute:.0f}** each week. A **{trend_type}** slope indicates a **{trend_direction_word}** trend, suggesting that **{trend_implication}** as time progresses.
                3. **Peak and Low Periods**: The height of the bars relative to the average line reveals periods of **{"increased" if slope > 0 else "decreased"}** data collection. Bars above the average line indicate peak periods, where more records were collected than usual. Conversely, bars below the average line suggest low periods, which might be influenced by external factors such as holidays, system downtimes, or changes in user engagement patterns.
                """)

    with row1_col2:
        # Filtro de país para o gráfico de análise de sentimento
        selected_country_2 = st.selectbox('Select Country for Sentiment Analysis',
                                          available_countries, format_func=lambda x: country_mapping.get(x, x))

        # Filtrar o DataFrame original com base no país selecionado
        filtered_df_2 = filtered_df.copy()
        if selected_country_2 != 'All':
            filtered_df_2 = filtered_df_2[filtered_df_2['country_code'] == selected_country_2]

        filtered_sentiment_counts = filtered_df_2.groupby(
            'year_week')['cleaned_sentiment'].agg(['mean', 'count']).reset_index()
        filtered_sentiment_counts['week_number'] = filtered_sentiment_counts['year_week'].dt.week

        # Check if filtered_sentiment_counts is empty
        if filtered_sentiment_counts.empty:
            st.warning(
                "No data available for the selected combination of country and feedback type.")
        else:
            # Gráfico de Análise de Sentimento ao longo do tempo
            fig2, ax2 = plt.subplots(figsize=(10, 6))
            fig2.patch.set_facecolor('#0e1117')
            ax2.set_facecolor('#262730')

            vmin = filtered_sentiment_counts['mean'].min()
            vmax = filtered_sentiment_counts['mean'].max()

            # Red to Yellow to Green
            colors = ['#ff4b4b', '#ffdc00', '#02b99d']
            cmap = mcolors.LinearSegmentedColormap.from_list(
                "custom", colors, N=100)

            scatter = ax2.scatter(filtered_sentiment_counts['week_number'], filtered_sentiment_counts['mean'],
                                  c=filtered_sentiment_counts['mean'], cmap=cmap,
                                  vmin=vmin, vmax=vmax, s=filtered_sentiment_counts['count']/10)

            cbar = plt.colorbar(scatter, label='Sentiment Score')
            cbar.ax.tick_params(labelcolor='white')
            cbar.set_label('Sentiment Score', color='white')
            cbar.set_ticks([vmin, (vmin + vmax) / 2, vmax])
            cbar.set_ticklabels(['Negative', 'Neutral', 'Positive'])

            x = filtered_sentiment_counts['week_number']
            y = filtered_sentiment_counts['mean']
            z = np.polyfit(x, y, 1)
            p = np.poly1d(z)
            ax2.plot(x, p(x), "r--", label='Trend')

            slope = z[0]
            slope_percentage = slope * 100

            # Define trend_direction based on the slope
            trend_direction = "increased" if slope > 0 else "decreased"

            # Define sentiment_change based on the slope
            sentiment_change = "improvement" if slope > 0 else "decline"

            # Calculate annual percentage change
            annual_percentage_change = slope_percentage * 52  # Assuming 52 weeks in a year

            # Calculate highest and lowest sentiment values
            highest_sentiment = filtered_sentiment_counts['mean'].max()
            lowest_sentiment = filtered_sentiment_counts['mean'].min()

            # Find the weeks with highest and lowest sentiment
            week_highest_sentiment = filtered_sentiment_counts.loc[
                filtered_sentiment_counts['mean'] == highest_sentiment, 'week_number'].iloc[0]
            week_lowest_sentiment = filtered_sentiment_counts.loc[
                filtered_sentiment_counts['mean'] == lowest_sentiment, 'week_number'].iloc[0]

            # Calculate largest and smallest count values
            largest_count = filtered_sentiment_counts['count'].max()
            smallest_count = filtered_sentiment_counts['count'].min()

            # Find the weeks with largest and smallest count
            week_largest_count = filtered_sentiment_counts.loc[
                filtered_sentiment_counts['count'] == largest_count, 'week_number'].iloc[0]
            week_smallest_count = filtered_sentiment_counts.loc[
                filtered_sentiment_counts['count'] == smallest_count, 'week_number'].iloc[0]

            # Calculate outliers
            z_scores = np.abs((filtered_sentiment_counts['mean'] - filtered_sentiment_counts['mean'].mean(
            )) / filtered_sentiment_counts['mean'].std())
            outliers = filtered_sentiment_counts[z_scores > 2]

            slope_text = f'Slope: {slope:.4f} (approx. {abs(
                slope_percentage):.2f}% change per week)'
            ax2.text(0.05, 0.95, slope_text, transform=ax2.transAxes,
                     color='white', fontweight='bold', verticalalignment='top')

            ax2.set_ylim(vmin - 0.1, vmax + 0.1)
            ax2.set_xticks(filtered_sentiment_counts['week_number'])
            ax2.set_xticklabels(
                filtered_sentiment_counts['week_number'], rotation=45, ha='right')

            ax2.set_title('Weekly Sentiment Analysis', color='white')
            ax2.set_xlabel('Week Number', color='white')
            ax2.set_ylabel('Average Sentiment', color='white')
            ax2.tick_params(axis='x', colors='white')
            ax2.tick_params(axis='y', colors='white')
            ax2.legend().set_visible(False)
            plt.tight_layout()
            st.pyplot(fig2, use_container_width=True)

            st.write("### Interpreting Weekly Sentiment Analysis")
            st.write("This graph shows the average sentiment over time:")
            with st.expander("See explanation"):
                st.write(f"""
                1. **Trend**: The red dashed line shows the overall trend in sentiment. The sentiment has {trend_direction} over time, with a slope of {slope:.4f}, indicating an approximate {abs(slope_percentage):.2f}% {sentiment_change} in sentiment per week. This suggests an annual {sentiment_change} of about {abs(annual_percentage_change):.2f}%.

                2. **Highest and Lowest Points**: 
                   - The highest average sentiment ({highest_sentiment:.2f}) was observed in week {week_highest_sentiment}.
                   - The lowest average sentiment ({lowest_sentiment:.2f}) was observed in week {week_lowest_sentiment}.

                3. **Data Volume**: 
                   - The largest number of records ({largest_count}) was collected in week {week_largest_count}.
                   - The smallest number of records ({smallest_count}) was collected in week {week_smallest_count}.

                4. **Color Coding**: The color of each point represents the sentiment score, with red indicating negative sentiment, yellow neutral, and green positive sentiment.

                5. **Point Size**: The size of each point represents the number of records for that week, with larger points indicating more data.
                """)

                # Add outlier information inside the expander
                if not outliers.empty:
                    st.write("**Outliers:**")
                    for _, outlier in outliers.iterrows():
                        st.write(f"Week {outlier['week_number']}: Sentiment score of {outlier['mean']:.2f}")
                    st.write("These deviations could indicate external factors or events that influenced sentiment significantly, such as market changes, policy shifts, or social events.")

    with row2_col1:
        # Total Distribution by Country
        country_distribution = filtered_df['country_code'].value_counts()
        fig3, ax3 = plt.subplots(figsize=(12, 6))
        fig3.patch.set_facecolor('#0e1117')  # Cor de fundo da figura
        ax3.set_facecolor('#262730')  # Cor de fundo do eixo
        bars = ax3.barh(country_distribution.index, country_distribution.values, color=[
                        '#009079', '#cc9300', '#642f7a'])

        for i, (country, v) in enumerate(country_distribution.items()):
            percentage = (v / country_distribution.sum()) * 100
            ax3.text(v, i, f' {percentage:.1f}%', va='center',
                     ha='left', fontweight='bold', color='white', fontsize=12)

        # Ajustar o comprimento das barras para começar no valor zero
        ax3.set_xlim(left=0)
        ax3.set_yticks(range(len(country_distribution)))  # Rótulos do eixo Y
        ax3.set_yticklabels(country_distribution.index, color='white')
        ax3.set_xlabel('Count', color='white')  # Eixo X em branco
        ax3.set_ylabel('Country', color='white')  # Eixo Y em branco
        ax3.tick_params(axis='x', colors='white')
        ax3.tick_params(axis='y', colors='white')

        plt.tight_layout()
        st.pyplot(fig3, use_container_width=True)

        st.write("### Interpreting Total Distribution by Country")
        st.write(
            "This bar chart illustrates the distribution of records across countries:")
        with st.expander("See explanation"):
            st.write("""
            1. **Country Distribution**: Each bar represents the total records per country, enabling straightforward comparison.
            2. **Percentage Representation**: The percentage labels highlight each country's share of the total records.
            3. **Market Insights**: Longer bars reveal countries with a higher concentration of records, indicating larger or more active markets.
            4. **Data Balance**: The bar lengths reflect the distribution balance across countries, offering insights into data coverage.
            """)

    with row2_col2:
        # Country Distribution Over Time
        fig4, ax4 = plt.subplots(figsize=(10, 6))
        fig4.patch.set_facecolor('#0e1117')  # Cor de fundo da figura
        ax4.set_facecolor('#262730')  # Cor de fundo do eixo
        country_time_distribution_percentage.plot(
            kind='area', stacked=True, ax=ax4, color=['#009079', '#cc9300', '#642f7a'])

        ax4.set_title('Country Distribution Over Time',
                      color='white')  # Título em branco
        ax4.set_xlabel('Week', color='white')  # Eixo X em branco
        ax4.set_ylabel('Percentage', color='white')  # Eixo Y em branco

        legend = ax4.legend(title='Country', bbox_to_anchor=(1.05, 1), loc='upper left',
                            facecolor='black', edgecolor='white', fontsize='medium')
        legend.get_title().set_color('white')  # Título da legenda em branco
        for text in legend.get_texts():  # Alterar a cor do texto da legenda
            text.set_color('white')

        ax4.tick_params(axis='x', colors='white')
        ax4.tick_params(axis='y', colors='white')
        plt.xticks(rotation=45, ha='right', color='white')

        plt.tight_layout()
        st.pyplot(fig4, use_container_width=True)

        st.write("### Interpreting Country Distribution Over Time")

        st.write(
            "This stacked area chart tracks changes in the distribution of records across countries over time:")

        with st.expander("See explanation"):

            st.write("""

            1. **Temporal Dynamics**: Observe how the share of records for each country evolves week by week.

            2. **Market Movements**: Significant shifts in the areas may indicate changes in market activity or data collection focus.

            3. **Consistency Indicators**: Stable areas suggest a consistent approach to data collection across different periods.
            4. **Seasonal Effects**: Identify recurring patterns that might point to seasonal influences on data distribution.

            5. **Data Collection Variations**: Notice any abrupt changes that could signal adjustments in data collection methods or shifts in market strategy.

            """)

    # Word Cloud Analysis
    st.header('Word Clouds: Comparing Original and Cleaned Text')
    st.markdown("<hr style='border: 1px solid #00c3a5;'>",
                unsafe_allow_html=True)

    # Contar palavras
    all_text = ' '.join(filtered_df['cleaned_content'].fillna(''))
    word_freq = count_words(all_text)

    # Gerar nuvem de palavras
    wordcloud_image = generate_wordcloud(
        word_freq, 'Cleaned Text Word Cloud', filtered_df)

    # Criar DataFrame com as palavras mais comuns
    most_common_words = pd.DataFrame(
        word_freq.most_common(10), columns=['Word', 'Count'])
    most_common_words['Percentage'] = most_common_words['Count'].apply(
        lambda x: f"{(x / most_common_words['Count'].sum() * 100):.2f}%")
    most_common_words.index = range(1, len(most_common_words) + 1)
    most_common_words.index.name = 'Rank'

    col1, col2 = st.columns(2)

    with col1:
        # Filtro de país para o gráfico de palavras mais comuns no texto original
        selected_country_original = st.selectbox(
            'Select Country for Original Text Analysis', country_options)

        # Filtrar o DataFrame original com base no país selecionado
        if selected_country_original == 'All':
            filtered_df_original = df
        else:
            selected_country_abbr = [abbr for abbr, name in country_mapping.items(
            ) if name == selected_country_original][0]
            filtered_df_original = df[df['country_code']
                                      == selected_country_abbr]

        original_text = ' '.join(filtered_df_original['content_en'].fillna(''))
        original_word_freq = count_words(original_text)
        original_wordcloud_image = generate_wordcloud(
            original_word_freq, 'Original Text Word Cloud', filtered_df_original)

        st.image(f"data:image/png;base64,{original_wordcloud_image}",
                 caption='Original Text Word Cloud', use_column_width=True)

        st.write("### Most Common Words in Original Text")
        st.write(
            "The table below shows the top 10 most frequent words in the original, unprocessed text:")

        most_common_words_original = pd.DataFrame(
            original_word_freq.most_common(10), columns=['Word', 'Count'])
        most_common_words_original['Percentage'] = most_common_words_original['Count'].apply(
            lambda x: f"{(x / most_common_words_original['Count'].sum() * 100):.2f}%")
        most_common_words_original.index = range(
            1, len(most_common_words_original) + 1)
        most_common_words_original.index.name = 'Rank'

        def format_table(df):
            return df.style.set_properties(**{
                'text-align': 'center',
                'font-size': '14px',
                'border-color': 'darkgrey'
            }).set_table_styles([
                {'selector': 'th', 'props': [
                    ('text-align', 'center'), ('font-weight', 'bold')]},
                {'selector': 'caption', 'props': [('caption-side', 'top')]}
            ]).hide(axis="index")

        st.dataframe(format_table(most_common_words_original),
                     use_container_width=True)
        
        audit_result_original = audit_data(
            original_word_freq, most_common_words_original)
        if "Inconsistency detected" in audit_result_original:
            st.error(f"❌ {audit_result_original}")
        else:
            st.success(f"✅ {audit_result_original}")

        st.write("### Interpreting the Original Text Word Cloud")
        st.write(
            "This word cloud represents the most frequent words in the original, unprocessed text.")

        with st.expander("See explanation"):

            st.write("""
            1. **Prominence of Common Words**: Words like 'you', 'the', 'and', 'to' are very prominent. These are typically stopwords that don't carry much meaning on their own.
            2. **Context Clues**: Words like 'Dr', 'appointment', and 'message' suggest that the text is related to medical or healthcare communications.
            3. **Potential Noise**: The presence of numbers (e.g., '2024') and short words might indicate dates or other non-contextual information.
            4. **Limited Insight**: While this cloud gives us an overview, it's harder to extract meaningful insights due to the presence of common, less informative words.
            """)

    with col2:
        # Filtro de país para o gráfico de palavras mais comuns no texto limpo
        selected_country_cleaned = st.selectbox(
            'Select Country for Cleaned Text Analysis', country_options)

        if selected_country_cleaned == 'All':
            filtered_df_cleaned = df
        else:
            selected_country_abbr = [abbr for abbr, name in country_mapping.items(
            ) if name == selected_country_cleaned][0]
            filtered_df_cleaned = df[df['country_code']
                                     == selected_country_abbr]

        all_text_cleaned = ' '.join(
            filtered_df_cleaned['cleaned_content'].fillna(''))
        word_freq_cleaned = count_words(all_text_cleaned)

        wordcloud_image_cleaned = generate_wordcloud(
            word_freq_cleaned, 'Cleaned Text Word Cloud', filtered_df_cleaned)

        st.image(f"data:image/png;base64,{wordcloud_image_cleaned}",
                 caption='Cleaned Text Word Cloud', use_column_width=True)

        st.write("### Most Common Words in Cleaned Text")
        st.write(
            "The table below shows the top 10 most frequent words after text cleaning and preprocessing:")

        most_common_words_cleaned = pd.DataFrame(
            word_freq_cleaned.most_common(10), columns=['Word', 'Count'])
        most_common_words_cleaned['Percentage'] = most_common_words_cleaned['Count'].apply(
            lambda x: f"{(x / most_common_words_cleaned['Count'].sum() * 100):.2f}%")
        most_common_words_cleaned.index = range(
            1, len(most_common_words_cleaned) + 1)
        most_common_words_cleaned.index.name = 'Rank'

        st.dataframe(format_table(most_common_words_cleaned),
                     use_container_width=True)
        
        audit_result_cleaned = audit_data(
            word_freq_cleaned, most_common_words_cleaned)
        if "Inconsistency detected" in audit_result_cleaned:
            st.error(f"❌ {audit_result_cleaned}")
        else:
            st.success(f"✅ {audit_result_cleaned}")

        st.write("### Interpreting the Cleaned Text Word Cloud")

        st.write("This word cloud shows the most frequent words after text cleaning and preprocessing. Notice the differences:")

        with st.expander("See explanation"):

            st.write("""

            1. **Removal of Stopwords**: Common words like 'the', 'and', 'to' have been removed, allowing more meaningful words to stand out.    
            2. **Emphasis on Key Terms**: Words like 'doctor', 'appointment', 'email', and 'contact' are now more prominent, giving us a clearer picture of the main topics.
            3. **Emergence of Insights**: We can now see terms like 'unsubscribe', 'opinion', and 'specialist' more clearly, which might indicate user concerns or common actions.
            4. **Cleaner Representation**: The absence of numbers and short, less meaningful words allows for a more focused analysis of the content.
            5. **Potential Themes**: Words like 'consultation', 'visit', and 'appointment' suggest that scheduling and medical visits are frequent topics in the feedback.
            """)

    # Gráfico de Distribuição de Sentimentos
    st.header('Sentiment Distribution')
    st.markdown("<hr style='border: 1px solid #00c3a5;'>",
                unsafe_allow_html=True)
    st.write(
        "Sentiment Score: Ranges from -1 (very negative) to +1 (very positive); 0 is neutral")
    col3, col4 = st.columns(2)

    with col3:
        selected_country_original_sentiment = st.selectbox(
            'Select Country for Original Sentiment Distribution', country_options)

        if selected_country_original_sentiment == 'All':
            filtered_df_sentiment_original = df
        else:
            selected_country_abbr = [abbr for abbr, name in country_mapping.items(
            ) if name == selected_country_original_sentiment][0]
            filtered_df_sentiment_original = df[df['country_code']
                                                == selected_country_abbr]

        fig1, ax1 = plt.subplots(figsize=(10, 5))
        fig1.patch.set_facecolor('#0e1117')  # Cor de fundo da figura
        ax1.set_facecolor('#262730')  # Cor de fundo do eixo
        filtered_df_sentiment_original['original_sentiment'].hist(
            ax=ax1, bins=50, alpha=0.7, color='#1f77b4', label='Original Sentiment')
        ax1.set_xlabel('Sentiment Score', color='white')
        ax1.set_ylabel('Frequency', color='white')
        ax1.set_title('Original Sentiment Distribution', color='white')
        ax1.tick_params(axis='x', colors='white')
        ax1.tick_params(axis='y', colors='white')
        legend1 = ax1.legend(facecolor='black', edgecolor='white')
        for text in legend1.get_texts():
            text.set_color('white')
        plt.tight_layout()
        st.pyplot(fig1, use_container_width=True)

        mean_original = filtered_df_sentiment_original['original_sentiment'].mean(
        )
        median_original = filtered_df_sentiment_original['original_sentiment'].median(
        )
        positive_percent = (
            filtered_df_sentiment_original['original_sentiment'] > 0).mean() * 100
        negative_percent = (
            filtered_df_sentiment_original['original_sentiment'] < 0).mean() * 100
        neutral_percent = (
            filtered_df_sentiment_original['original_sentiment'] == 0).mean() * 100

        sentiment_meaning = 'The texts are generally positive' if mean_original > 0 else 'The texts are generally negative' if mean_original < 0 else 'The texts are mostly neutral'
        balance_opinion = 'There\'s a good balance of opinions' if abs(positive_percent - negative_percent) < 10 else f'There\'s a clear tendency towards {
            "positive" if positive_percent > negative_percent else "negative"} sentiment'

        st.write("### Interpreting the Original Sentiment Distribution")
        st.write(
            "This histogram displays the distribution of sentiment scores before text cleaning.")

        with st.expander("See explanation"):

            st.write(f"""

            1. **Key Findings**:

               - Average (mean) sentiment: {mean_original:.2f}
               - Middle (median) sentiment: {median_original:.2f}

               - {positive_percent:.1f}% of texts are positive

               - {negative_percent:.1f}% of texts are negative

               - {neutral_percent:.1f}% of texts are neutral


            2. **What This Means**:
               - {sentiment_meaning}
               - {balance_opinion}


            3. **Why It Matters**:

               - This helps us understand the overall tone of the original texts.

               - It can indicate how people initially express their feelings about the topic discussed.

            """)

    with col4:
        selected_country_cleaned_sentiment = st.selectbox(
            'Select Country for Cleaned Sentiment Distribution', country_options)

        if selected_country_cleaned_sentiment == 'All':
            filtered_df_sentiment_cleaned = df
        else:
            selected_country_abbr = [abbr for abbr, name in country_mapping.items(
            ) if name == selected_country_cleaned_sentiment][0]
            filtered_df_sentiment_cleaned = df[df['country_code']
                                               == selected_country_abbr]

        fig2, ax2 = plt.subplots(figsize=(10, 5))
        fig2.patch.set_facecolor('#0e1117')
        ax2.set_facecolor('#262730')
        filtered_df_sentiment_cleaned['cleaned_sentiment'].hist(
            ax=ax2, bins=50, alpha=0.7, color='#00c3a5', label='Cleaned Sentiment')
        ax2.set_xlabel('Sentiment Score', color='white')
        ax2.set_ylabel('Frequency', color='white')
        ax2.set_title('Cleaned Sentiment Distribution', color='white')
        ax2.tick_params(axis='x', colors='white')
        ax2.tick_params(axis='y', colors='white')
        legend2 = ax2.legend(facecolor='black', edgecolor='white')
        for text in legend2.get_texts():
            text.set_color('white')
        plt.tight_layout()
        st.pyplot(fig2, use_container_width=True)

        mean_cleaned = filtered_df_sentiment_cleaned['cleaned_sentiment'].mean(
        )
        median_cleaned = filtered_df_sentiment_cleaned['cleaned_sentiment'].median(
        )
        positive_percent_cleaned = (
            filtered_df_sentiment_cleaned['cleaned_sentiment'] > 0).mean() * 100
        negative_percent_cleaned = (
            filtered_df_sentiment_cleaned['cleaned_sentiment'] < 0).mean() * 100
        neutral_percent_cleaned = (
            filtered_df_sentiment_cleaned['cleaned_sentiment'] == 0).mean() * 100

        st.write("### Interpreting the Cleaned Sentiment Distribution")

        st.write(
            "This histogram displays the distribution of sentiment scores after text cleaning.")

        with st.expander("See explanation"):

            st.write(f"""\

            1. **Key Findings After Cleaning**:

               - Average (mean) sentiment: {mean_cleaned:.2f}

               - Middle (median) sentiment: {median_cleaned:.2f}

               - {positive_percent_cleaned:.1f}% of texts are positive
               - {negative_percent_cleaned:.1f}% of texts are negative

               - {neutral_percent_cleaned:.1f}% of texts are neutral


            2. **What Changed**:

               - {'The cleaning process has generally made the sentiment more positive' if mean_cleaned > mean_original else 'The cleaning process has generally made the sentiment more negative' if mean_cleaned < mean_original else 'The cleaning process has not significantly changed the overall sentiment'}.
               - The percentage of {'positive' if positive_percent_cleaned > positive_percent else 'negative' if negative_percent_cleaned > negative_percent else 'neutral'} texts has increased after cleaning.

            3. **Why It Matters**:
               - Cleaning the text can reveal underlying sentiments that might be obscured by noise or common phrases.
               - The difference between original and cleaned sentiment can show how much the non-essential parts of the text were influencing the sentiment analysis.
            """)

    # Add this line where you want to display the text length comparison
    display_text_length_comparison(df)


    # Call the display_categorized_data function
    display_categorized_data(df, country_options, country_mapping)

    # # Chama a função para exibir o diagrama
    # display_diagram()  # Chamada da função

# Adicione esta linha no final do arquivo
__all__ = ['run_data_categorization']

if __name__ == "__main__":
    run_data_categorization()
