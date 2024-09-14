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
    # Adicionando filtro para category_bert com uma chave única
    categories = ['All'] + sorted(df['category_bert'].unique().tolist())
    selected_category = st.selectbox(f'Select Touchpoint', categories, key=f"touchpoint_{metric}")
    
    filtered_df = df if selected_category == 'All' else df[df['category_bert'] == selected_category]
    
    # Convertendo 'created_at' para datetime se ainda não estiver
    filtered_df['created_at'] = pd.to_datetime(filtered_df['created_at'])
    
    # Criando coluna year_week
    filtered_df['year_week'] = filtered_df['created_at'].dt.to_period('W').astype(str)
    
    # Agrupando os dados
    filtered_sentiment_counts = filtered_df.groupby('year_week')['cleaned_sentiment'].agg(['mean', 'count']).reset_index()
    
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

        all_weeks = filtered_sentiment_counts['week_number'] + (filtered_sentiment_counts['year'] - filtered_sentiment_counts['year'].min()) * 52

        scatter = ax.scatter(all_weeks, 
                             filtered_sentiment_counts['mean'],
                             c=filtered_sentiment_counts['mean'], cmap=cmap,
                             vmin=vmin, vmax=vmax, s=filtered_sentiment_counts['count']/10,  # Reduzido o tamanho dos círculos
                             label='Sentiment')

        cbar = plt.colorbar(scatter, label='Sentiment Score')
        cbar.ax.tick_params(labelcolor='white')
        cbar.set_label('Sentiment Score', color='white')
        cbar.set_ticks([vmin, (vmin + vmax) / 2, vmax])
        cbar.set_ticklabels(['Negative', 'Neutral', 'Positive'])

        # Linha verde para o valor mais alto
        max_sentiment = filtered_sentiment_counts['mean'].max()
        ax.axhline(y=max_sentiment, color='#00c3a5', linestyle='-', label='Highest Value', linewidth=1.5)

        x = all_weeks
        y = filtered_sentiment_counts['mean']
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        ax.plot(x, p(x), "r--", label='Trend')

        slope = z[0]
        slope_percentage = slope * 100

        current_mean = filtered_df['cleaned_sentiment'].mean()
        benchmark_value = max_sentiment

        ax.set_ylim(vmin - 0.1, vmax + 0.1)
        ax.set_xticks(range(1, 53, 13))
        ax.set_xticklabels(range(1, 53, 13), rotation=45, ha='right')

        ax.set_title(title, color='white', fontsize=10)
        ax.set_xlabel('Week Number', color='white', fontsize=8)
        ax.set_ylabel('Average Sentiment', color='white', fontsize=8)
        ax.tick_params(axis='x', colors='white', labelsize=6)
        ax.tick_params(axis='y', colors='white', labelsize=6)

        # Configurando a legenda sem o ano
        legend = ax.legend(fontsize='6', loc='lower left')
        legend.get_frame().set_facecolor('#262730')
        legend.get_frame().set_edgecolor('none')
        for text in legend.get_texts():
            text.set_color('white')

        plt.tight_layout()
        st.pyplot(fig)

        # Calculando a diferença percentual entre a média e o benchmark
        percentage_difference = ((benchmark_value - current_mean) / current_mean) * 100

        # Exibindo a média, o benchmark e a diferença percentual
        st.markdown(f"<p style='color: #00c3a5;'>Average: {current_mean:.2f} | Benchmark: {benchmark_value:.2f} | Difference: {percentage_difference:.2f}%</p>", unsafe_allow_html=True)

        with st.expander("See explanation"):
            st.write(f"""
            This graph shows the trend of cleaned sentiment over time:
            1. **Trend:** The red dashed line represents the overall trend in cleaned sentiment. 
               The slope of {slope:.4f} indicates that the average cleaned sentiment 
               {"increased" if slope > 0 else "decreased"} by approximately {abs(slope_percentage):.2f}% each week.
            2. **Weekly Sentiment:** Each point represents the average cleaned sentiment for a specific week.
            3. **Data Volume:** Larger points indicate more data for that week.
            4. **Year Comparison:** Different colors represent different years for easy comparison.
            5. **Highest Value:** The green line represents the highest sentiment value.
            """)

if __name__ == "__main__":
    # Este bloco só será executado se o script for executado diretamente
    # Você pode adicionar código de teste aqui se necessário
    pass

