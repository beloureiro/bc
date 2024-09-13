import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import pandas as pd

def grafico_meta(df):
    # Adicionando o título em inglês acima de todos os gráficos
    st.write("## Defining the Process Goal")
    
    # Criando três colunas para os gráficos
    col1, col2, col3 = st.columns(3)
    
    # Lista de métricas para os gráficos
    metrics = ['original_sentiment', 'cleaned_sentiment', 'sentiment_difference']
    titles = ['Original Sentiment', 'Cleaned Sentiment', 'Sentiment Difference']
    
    for i, (metric, title, col) in enumerate(zip(metrics, titles, [col1, col2, col3])):
        with col:
            create_sentiment_chart(df, metric, title)

def create_sentiment_chart(df, metric, title):
    # Adicionando filtro para category_bert
    categories = ['All'] + sorted(df['category_bert'].unique().tolist())
    selected_category = st.selectbox(f'Select Category for {title}', categories)
    
    filtered_df = df if selected_category == 'All' else df[df['category_bert'] == selected_category]
    
    # Convertendo 'created_at' para datetime se ainda não estiver
    filtered_df['created_at'] = pd.to_datetime(filtered_df['created_at'])
    
    # Criando coluna year_week
    filtered_df['year_week'] = filtered_df['created_at'].dt.to_period('W').astype(str)
    
    # Agrupando os dados
    filtered_sentiment_counts = filtered_df.groupby('year_week')[metric].agg(['mean', 'count']).reset_index()
    
    # Extraindo a data de início da semana a partir de year_week
    filtered_sentiment_counts['week_start'] = pd.to_datetime(filtered_sentiment_counts['year_week'].str.split('/').str[0])
    filtered_sentiment_counts['week_number'] = filtered_sentiment_counts['week_start'].dt.isocalendar().week
    filtered_sentiment_counts['year'] = filtered_sentiment_counts['week_start'].dt.year

    if not filtered_sentiment_counts.empty:
        fig, ax = plt.subplots(figsize=(4, 3))
        fig.patch.set_facecolor('#0e1117')
        ax.set_facecolor('#262730')

        vmin = filtered_sentiment_counts['mean'].min()
        vmax = filtered_sentiment_counts['mean'].max()

        colors = ['#ff4b4b', '#ffdc00', '#02b99d']
        cmap = mcolors.LinearSegmentedColormap.from_list("custom", colors, N=100)

        for year in filtered_sentiment_counts['year'].unique():
            year_data = filtered_sentiment_counts[filtered_sentiment_counts['year'] == year]
            scatter = ax.scatter(year_data['week_number'], year_data['mean'],
                                 c=year_data['mean'], cmap=cmap,
                                 vmin=vmin, vmax=vmax, s=year_data['count']/10,
                                 label=str(year))

        cbar = plt.colorbar(scatter, label='Sentiment Score')
        cbar.ax.tick_params(labelcolor='white')
        cbar.set_label('Sentiment Score', color='white')
        cbar.set_ticks([vmin, (vmin + vmax) / 2, vmax])
        cbar.set_ticklabels(['Negative', 'Neutral', 'Positive'])

        x = filtered_sentiment_counts['week_number']
        y = filtered_sentiment_counts['mean']
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        ax.plot(x, p(x), "r--", label='Trend')

        slope = z[0]
        slope_percentage = slope * 100

        slope_text = f'Slope: {slope:.4f}\n({abs(slope_percentage):.2f}% change/week)'
        ax.text(0.05, 0.95, slope_text, transform=ax.transAxes,
                color='white', fontweight='bold', verticalalignment='top', fontsize=8)

        ax.set_ylim(vmin - 0.1, vmax + 0.1)
        ax.set_xticks(range(1, 53, 13))
        ax.set_xticklabels(range(1, 53, 13), rotation=45, ha='right')

        chart_title = f'{title}\n{selected_category}' if selected_category != 'All' else f'{title}\nAll Categories'
        ax.set_title(chart_title, color='white', fontsize=10)
        ax.set_xlabel('Week Number', color='white', fontsize=8)
        ax.set_ylabel('Average Sentiment', color='white', fontsize=8)
        ax.tick_params(axis='x', colors='white', labelsize=6)
        ax.tick_params(axis='y', colors='white', labelsize=6)
        ax.legend(title='Year', title_fontsize='8', fontsize='6', loc='lower left')
        plt.tight_layout()
        st.pyplot(fig)

        with st.expander("See explanation"):
            if metric == 'original_sentiment':
                st.write(f"""
                This graph shows the trend of original sentiment over time:
                1. **Trend:** The red dashed line represents the overall trend in original sentiment. 
                   The slope of {slope:.4f} indicates that the average original sentiment 
                   {"increased" if slope > 0 else "decreased"} by approximately {abs(slope_percentage):.2f}% each week.
                2. **Weekly Sentiment:** Each point represents the average original sentiment for a specific week.
                3. **Data Volume:** Larger points indicate more data for that week.
                4. **Year Comparison:** Different colors represent different years for easy comparison.
                """)
            elif metric == 'cleaned_sentiment':
                st.write(f"""
                This graph shows the trend of cleaned sentiment over time:
                1. **Trend:** The red dashed line represents the overall trend in cleaned sentiment. 
                   The slope of {slope:.4f} indicates that the average cleaned sentiment 
                   {"increased" if slope > 0 else "decreased"} by approximately {abs(slope_percentage):.2f}% each week.
                2. **Weekly Sentiment:** Each point represents the average cleaned sentiment for a specific week.
                3. **Data Volume:** Larger points indicate more data for that week.
                4. **Year Comparison:** Different colors represent different years for easy comparison.
                """)
            else:  # sentiment_difference
                st.write(f"""
                This graph shows the trend of sentiment difference over time:
                1. **Trend:** The red dashed line represents the overall trend in sentiment difference. 
                   The slope of {slope:.4f} indicates that the average sentiment difference 
                   {"increased" if slope > 0 else "decreased"} by approximately {abs(slope_percentage):.2f}% each week.
                2. **Weekly Difference:** Each point represents the average sentiment difference for a specific week.
                3. **Data Volume:** Larger points indicate more data for that week.
                4. **Year Comparison:** Different colors represent different years for easy comparison.
                """)

if __name__ == "__main__":
    # Este bloco só será executado se o script for executado diretamente
    # Você pode adicionar código de teste aqui se necessário
    pass

