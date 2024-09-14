def critical_points_function():
    import streamlit as st
    import pandas as pd
    import os

    # Get the current file's directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    data_dir = os.path.join(parent_dir, 'Data_Categorization')

    # Construct the paths to the new CSV files
    file_path_part1 = os.path.join(data_dir, 'processed_data_part1.csv')
    file_path_part2 = os.path.join(data_dir, 'processed_data_part2.csv')

    # Load the data
    try:
        df_part1 = pd.read_csv(file_path_part1, encoding='utf-8')
        df_part2 = pd.read_csv(file_path_part2, encoding='utf-8')
        df = pd.concat([df_part1, df_part2], ignore_index=True)
    except FileNotFoundError:
        st.error("One or both of the files 'processed_data_part1.csv' and 'processed_data_part2.csv' were not found. Please verify the path and try again.")
        return

    # Título principal
    st.title("Breakdown by Country: Critical Points")

    st.markdown("""
        Below are the <span style='color: #00c3a5;'><strong>critical points</strong></span>, which should be seen as <span style='color: #00c3a5;'><strong>prioritized touchpoints</strong></span>. These are identified based on their **frequency within the complaint database**, reflecting the areas of the process that most often impact patient experience. This stage supports the next one, which is focused on identifying the **root causes** of these prioritized results. You can explore customer feedback by country, viewing the total number of reviews, average sentiment, and urgent cases, as well as using filters to gain detailed insights into the areas that need the most attention.
        """, unsafe_allow_html=True)

    # Define country options
    country_column = 'country_code'
    # Create a dictionary mapping country codes to country names
    country_names = {
        'br': 'Brazil',
        'es': 'Spain',
        'de': 'Germany'
    }
    df['country_name'] = df[country_column].map(country_names)
    country_options = ['All'] + sorted(country_names.values())

    # Criar três colunas para os filtros
    col_country, col_sentiment, col_urgency = st.columns(3)

    with col_country:
        # Country selection usando os nomes dos países, com "All" como padrão
        selected_country_name = st.selectbox("Select a country", country_options, index=0)

    with col_sentiment:
        # Criar classificação de sentimento
        df['sentiment_classification'] = pd.cut(df['cleaned_sentiment'], 
                                                bins=[-1, -0.1, 0.1, 1], 
                                                labels=['Negative', 'Neutral', 'Positive'])
        
        selected_sentiments = st.multiselect(
            "Select Sentiments",
            options=['Positive', 'Neutral', 'Negative'],
            default=[]
        )

    with col_urgency:
        selected_urgency = st.multiselect(
            "Select Urgency Level",
            options=sorted(df['urgency_level'].unique()),
            default=[]
        )

    # Filtrar dados com base na seleção
    if selected_country_name == 'All':
        country_data = df  # Usar todos os dados se "All" for selecionado
    else:
        country_data = df[df['country_name'] == selected_country_name]

    # Aplicar filtro de sentimento
    if selected_sentiments:
        country_data = country_data[country_data['sentiment_classification'].isin(selected_sentiments)]

    # Aplicar filtro de urgência
    if selected_urgency:
        country_data = country_data[country_data['urgency_level'].isin(selected_urgency)]

    # Subtítulo com o país selecionado
    st.subheader(f"Analysis for: {selected_country_name}")
    
    # Calcular métricas
    total_reviews = int(country_data.shape[0])
    average_sentiment = float(country_data['cleaned_sentiment'].mean())
    
    # Calcular a porcentagem de casos de alta urgência
    high_urgency_percentage = float((country_data['urgency_level'] == 'High').mean() * 100)

    # Criar três colunas para os KPIs principais
    kpi1, kpi2, kpi3 = st.columns(3)
    
    with kpi1:
        st.metric("Total Reviews", f"{total_reviews:,}")
    with kpi2:
        st.metric("Avg Sentiment (-1 to 1)", f"{average_sentiment:.2f}")
    with kpi3:
        st.metric("High Urgency Cases", f"{high_urgency_percentage:.1f}%")

    # Adicionar uma linha para separar os KPIs das informações adicionais
    st.markdown("---")

    # Função para criar colunas de progresso
    def create_progress_column(dataframe, column_name):
        max_value = dataframe[column_name].sum()
        percentage = dataframe[column_name].apply(lambda x: (x / max_value) * 100)
        cumulative = dataframe[column_name].cumsum().apply(lambda x: (x / max_value) * 100)
        return percentage, cumulative

    # Criar duas colunas principais para BERT e Keywords Touchpoints
    col_bert, col_keywords = st.columns(2)

    with col_bert:
        st.subheader("BERT Touchpoints Ranking")
        category_counts_bert = country_data['category_bert'].value_counts().reset_index()
        category_counts_bert.columns = ['Touchpoint', 'Count']
        category_counts_bert['Touchpoint'] = category_counts_bert['Touchpoint'].astype(str)
        category_counts_bert['Percentage'], category_counts_bert['Cumulative'] = create_progress_column(category_counts_bert, 'Count')
        
        # Adicionar coluna de Rank
        category_counts_bert['Rank'] = range(1, len(category_counts_bert) + 1)
        
        # Reordenar as colunas para que Rank seja a primeira
        category_counts_bert = category_counts_bert[['Rank', 'Touchpoint', 'Count', 'Percentage', 'Cumulative']]

        st.dataframe(
            category_counts_bert,
            column_config={
                "Rank": st.column_config.NumberColumn("Rank", format="%d"),
                "Touchpoint": st.column_config.TextColumn("Touchpoint"),
                "Count": st.column_config.NumberColumn("Count"),
                "Percentage": st.column_config.ProgressColumn(
                    "Percentage",
                    format="%0.2f%%",
                    min_value=0,
                    max_value=100
                ),
                "Cumulative": st.column_config.ProgressColumn(
                    "Cumulative",
                    format="%0.2f%%",
                    min_value=0,
                    max_value=100
                ),
            },
            hide_index=True,
            use_container_width=True
        )

    with col_keywords:
        st.subheader("Keywords Touchpoints Ranking")
        category_counts_keywords = country_data['category_keywords'].value_counts().reset_index()
        category_counts_keywords.columns = ['Touchpoint', 'Count']
        category_counts_keywords['Touchpoint'] = category_counts_keywords['Touchpoint'].astype(str)
        category_counts_keywords['Percentage'], category_counts_keywords['Cumulative'] = create_progress_column(category_counts_keywords, 'Count')
        
        # Adicionar coluna de Rank
        category_counts_keywords['Rank'] = range(1, len(category_counts_keywords) + 1)
        
        # Reordenar as colunas para que Rank seja a primeira
        category_counts_keywords = category_counts_keywords[['Rank', 'Touchpoint', 'Count', 'Percentage', 'Cumulative']]

        st.dataframe(
            category_counts_keywords,
            column_config={
                "Rank": st.column_config.NumberColumn("Rank", format="%d"),
                "Touchpoint": st.column_config.TextColumn("Touchpoint"),
                "Count": st.column_config.NumberColumn("Count"),
                "Percentage": st.column_config.ProgressColumn(
                    "Percentage",
                    format="%0.2f%%",
                    min_value=0,
                    max_value=100
                ),
                "Cumulative": st.column_config.ProgressColumn(
                    "Cumulative",
                    format="%0.2f%%",
                    min_value=0,
                    max_value=100
                ),
            },
            hide_index=True,
            use_container_width=True
        )

    # Adicionar outra linha separadora
    st.markdown("---")

    # Tabela para Sentimentos
    st.subheader("Sentiment Distribution")
    # Criar uma classificação de sentimento baseada em cleaned_sentiment
    country_data['sentiment_classification'] = country_data['cleaned_sentiment'].apply(
        lambda x: 'Positive' if x > 0 else ('Negative' if x < 0 else 'Neutral')
    )
    sentiment_counts = country_data['sentiment_classification'].value_counts().reset_index()
    sentiment_counts.columns = ['Sentiment', 'Count']
    sentiment_counts['Sentiment'] = sentiment_counts['Sentiment'].astype(str)
    sentiment_counts['Percentage'], sentiment_counts['Cumulative'] = create_progress_column(sentiment_counts, 'Count')

    st.dataframe(
        sentiment_counts,
        column_config={
            "Sentiment": st.column_config.TextColumn("Sentiment"),
            "Count": st.column_config.NumberColumn("Count"),
            "Percentage": st.column_config.ProgressColumn(
                "Percentage",
                format="%0.2f%%",
                min_value=0,
                max_value=100
            ),
            "Cumulative": st.column_config.ProgressColumn(
                "Cumulative",
                format="%0.2f%%",
                min_value=0,
                max_value=100
            ),
        },
        hide_index=True,
        use_container_width=True
    )

    st.markdown("---")

    st.subheader("Filters and Detailed Data")

    # Criando filtros em uma única linha
    col1, col2, col3 = st.columns(3)

    with col1:
        selected_sentiments = st.multiselect(
            "Select Sentiments",
            options=country_data['sentiment_classification'].unique(),
            default=[]
        )

    with col2:
        selected_categories = st.multiselect(
            "BERT Touchpoints Classification",
            options=country_data['category_bert'].unique(),
            default=[]
        )

    with col3:
        selected_types = st.multiselect(
            "Keywords Touchpoints Classification",
            options=country_data['category_keywords'].unique(),
            default=[]
        )

    # Aplicando filtros
    filtered_data = country_data
    if selected_sentiments:
        filtered_data = filtered_data[filtered_data['sentiment_classification'].isin(selected_sentiments)]
    if selected_categories:
        filtered_data = filtered_data[filtered_data['category_bert'].isin(selected_categories)]
    if selected_types:
        filtered_data = filtered_data[filtered_data['category_keywords'].isin(selected_types)]

    # Exibindo a tabela filtrada em toda a largura da página
    st.subheader("Detailed Feedback Data")
    st.dataframe(
        filtered_data[[
            'content_en', 
            'cleaned_sentiment', 
            'sentiment_classification', 
            'category_bert', 
            'category_keywords', 
            'issue_type',
            'created_at',
            'resolution_suggestion'
        ]],
        column_config={
            "content_en": st.column_config.TextColumn("English Content"),
            "cleaned_sentiment": st.column_config.NumberColumn("Sentiment Score", format="%.4f"),
            "sentiment_classification": st.column_config.TextColumn("Sentiment"),
            "category_bert": st.column_config.TextColumn("BERT Category"),
            "category_keywords": st.column_config.TextColumn("Keywords Category"),
            "issue_type": st.column_config.TextColumn("Issue Type"),
            "created_at": st.column_config.DatetimeColumn("Date", format="DD/MM/YYYY"),
            "resolution_suggestion": st.column_config.TextColumn("Resolution Suggestion")
        },
        hide_index=True,
        use_container_width=True,
        height=400  # Você pode ajustar a altura conforme necessário
    )

