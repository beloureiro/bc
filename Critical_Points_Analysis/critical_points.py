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
    st.title("Breakdown by Country")

    # Dicionário para mapear países
    country_mapping = {
        'br': 'Brazil',
        'de': 'Germany',
        'es': 'Spain',
    }

    # Aplicar o mapeamento à coluna country_code
    df['country_name'] = df['country_code'].map(country_mapping)

    # Adicionar opção "All" à lista de países
    country_options = ['All'] + list(df['country_name'].unique())

    # Country selection usando os nomes dos países, com "All" como padrão
    selected_country_name = st.selectbox("Select a country", country_options, index=0)

    # Filtrar dados com base na seleção
    if selected_country_name == 'All':
        country_data = df  # Usar todos os dados se "All" for selecionado
        selected_country = "All Countries"
    else:
        # Obter o código do país selecionado
        selected_country = df[df['country_name'] == selected_country_name]['country_code'].iloc[0]
        country_data = df[df['country_code'] == selected_country]
        selected_country = selected_country_name  # Usar o nome do país para exibição

    # Subtítulo com o país selecionado
    st.subheader(f"Analysis for: {selected_country}")
    
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

        st.dataframe(
            category_counts_bert,
            column_config={
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

        st.dataframe(
            category_counts_keywords,
            column_config={
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

