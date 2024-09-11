import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

def prepare_country_distribution_data(filtered_df):
    country_time_distribution = filtered_df.groupby(
        ['year_week', 'country_code']).size().unstack(fill_value=0)
    country_time_distribution_percentage = country_time_distribution.div(
        country_time_distribution.sum(axis=1), axis=0)
    
    return country_time_distribution_percentage

def display_country_distribution(filtered_df):
    st.header('Country Distribution Analysis')
    st.markdown("<hr style='border: 1px solid #00c3a5;'>", unsafe_allow_html=True)

    country_time_distribution_percentage = prepare_country_distribution_data(filtered_df)

    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        display_total_distribution(filtered_df)

    with row2_col2:
        display_distribution_over_time(country_time_distribution_percentage)

def display_total_distribution(filtered_df):
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

    st.write("""
    ### Interpreting Total Distribution by Country

    This horizontal bar chart shows the distribution of records across different countries:

    1. **Country Comparison**: Each bar represents a country, allowing easy comparison of record counts.
    2. **Percentages**: The percentage next to each bar shows the proportion of total records from each country.
    3. **Dominant Markets**: Longer bars indicate countries with more records, possibly representing larger or more active markets.
    4. **Market Balance**: The relative sizes of the bars show how balanced or imbalanced the data collection is across countries.
    """)

def display_distribution_over_time(country_time_distribution_percentage):
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

    st.write("""
    ### Interpreting Country Distribution Over Time

    This stacked area chart shows how the distribution of records across countries changes over time:

    1. **Temporal Trends**: We can see how each country's proportion of records changes week by week.
    2. **Market Shifts**: Any significant changes in a country's area can indicate shifts in market activity or data collection practices.
    3. **Consistency**: Stable areas suggest consistent data collection across countries over time.
    4. **Seasonal Patterns**: Look for any recurring patterns that might indicate seasonal trends in different countries.
    5. **Data Collection Changes**: Sudden changes in proportions might reflect changes in data collection methods or market focus.
    """)