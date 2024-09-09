def critical_points_function():
    import streamlit as st
    import pandas as pd

    # Load the data
    # D:\OneDrive - InMotion - Consulting\DocPlanner\BusinessCase-Light\Data_Categorization
    try:
        df = pd.read_csv(
            'D:/OneDrive - InMotion - Consulting/DocPlanner/BusinessCase-Light/Data_Categorization/processed_data_categorized.csv')
    except FileNotFoundError:
        st.error(
            "The file 'processed_data_categorized.csv' was not found. Please verify the path and try again.")
        return

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
    selected_country_name = st.selectbox(
        "Select a country", country_options, index=0)

    # Filtrar dados com base na seleção
    if selected_country_name == 'All':
        country_data = df  # Usar todos os dados se "All" for selecionado
        selected_country = "All Countries"
    else:
        # Obter o código do país selecionado
        selected_country = df[df['country_name'] ==
                              selected_country_name]['country_code'].iloc[0]
        country_data = df[df['country_code'] == selected_country]
        selected_country = selected_country_name  # Usar o nome do país para exibição

    # Função para classificar o sentimento
    def classify_sentiment(score):
        if score < 0:
            return 'Negative'
        elif score == 0:
            return 'Neutral'
        else:
            return 'Positive'

    # Aplicar a classificação de sentimento
    country_data['sentiment_classification'] = country_data['cleaned_sentiment'].apply(
        classify_sentiment)

    # Calculate metrics
    total_reviews = int(country_data.shape[0])
    average_sentiment = float(country_data['cleaned_sentiment'].mean())
    # Changed from 'category' to 'category_bert'
    dominant_category = country_data['category_bert'].mode()[0]
    urgency_level = float(
        (country_data['issue_type'] == 'Critical').mean() * 100)
    doctors_mentioned = int(country_data['doctor_name'].nunique())
    hospitals_mentioned = int(country_data['hospital_name'].nunique())

    # Display KPIs at the top
    st.title(f"Country Analysis: {selected_country}")
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Total Reviews", total_reviews)
    kpi2.metric("Average Sentiment", f"{average_sentiment:.2f}")
    kpi3.metric("Dominant Category", dominant_category)

    kpi4, kpi5, kpi6 = st.columns(3)
    kpi4.metric("Urgency Level", f"{urgency_level:.1f}%")
    kpi5.metric("Doctors Mentioned", doctors_mentioned)
    kpi6.metric("Hospitals Mentioned", hospitals_mentioned)

    # Function to create a progress column
    def create_progress_column(dataframe, column_name):
        max_value = dataframe[column_name].sum()
        return dataframe[column_name].apply(
            lambda x: (x / max_value) * 100  # calculate percentage
        ), dataframe[column_name].cumsum().apply(
            lambda x: (x / max_value) * 100  # calculate cumulative percentage
        )

    # Table for Categories (without Count column)
    category_counts = country_data['category_bert'].value_counts(
    ).reset_index()  # Changed from 'category' to 'category_bert'
    category_counts.columns = ['Category', 'Count']
    category_counts['Category'] = category_counts['Category'].astype(str)
    category_counts['Percentage'], category_counts['Cumulative'] = create_progress_column(
        category_counts, 'Count')
    category_counts = category_counts.drop(columns=['Count'])

    # Table for Sentiments
    sentiment_counts = country_data['sentiment_classification'].value_counts(
    ).reset_index()
    sentiment_counts.columns = ['Sentiment', 'Count']
    sentiment_counts['Sentiment'] = sentiment_counts['Sentiment'].astype(str)
    sentiment_counts['Percentage'], sentiment_counts['Cumulative'] = create_progress_column(
        sentiment_counts, 'Count')

    # Display the tables in a grid
    st.subheader("Feedback Type Distribution")

    # Criar duas colunas principais
    col_left, col_right = st.columns(2)

    with col_left:
        # Coluna da esquerda para Category
        st.subheader("Category")

        # Tabela de Categorias (sem a coluna Count)
        st.data_editor(
            category_counts,
            column_config={
                "Category": st.column_config.TextColumn("Category"),
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
            disabled=True,
        )

    with col_right:
        # Coluna da direita para Sentiment
        st.subheader("Sentiment")

        # Tabela de Sentimentos
        st.data_editor(
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
            disabled=True,
        )

        # Aqui você pode adicionar outra tabela relevante, se necessário

    # Após as tabelas de Category e Sentiment

    st.subheader("Filters and Detailed Data")

    # Criando filtros
    col1, col2, col3 = st.columns(3)

    with col1:
        selected_sentiments = st.multiselect(
            "Select Sentiments",
            options=country_data['sentiment_classification'].unique(),
            default=[]
        )

    with col2:
        selected_categories = st.multiselect(
            "Patient Experience Issues (BERT)",
            options=country_data['category_bert'].unique(),
            default=[]
        )

    with col3:
        selected_types = st.multiselect(
            "Category keywords Issues",
            options=country_data['category_keywords'].unique(),
            default=[]
        )

    # Aplicando filtros
    filtered_data = country_data
    if selected_sentiments:
        filtered_data = filtered_data[filtered_data['sentiment_classification'].isin(
            selected_sentiments)]
    if selected_categories:
        filtered_data = filtered_data[filtered_data['category_bert'].isin(
            selected_categories)]
    if selected_types:
        filtered_data = filtered_data[filtered_data['category_keywords'].isin(
            selected_types)]

    # Exibindo a tabela filtrada
    st.subheader("Detailed Feedback Data")
    st.dataframe(
        # Removida a coluna 'cleaned_content'
        filtered_data[['content_en', 'cleaned_sentiment']],
        hide_index=True,
        column_config={
            "content_en": st.column_config.TextColumn("English Content"),
            "cleaned_sentiment": st.column_config.NumberColumn("Sentiment Score", format="%.4f")
        },
        height=400  # Você pode ajustar a altura conforme necessário
    )

    # The rest of the tables can follow in subsequent sections
