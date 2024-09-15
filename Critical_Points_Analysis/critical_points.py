import streamlit as st
import pandas as pd
import os

def critical_points_function():

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

    st.markdown("<h2 style='color: #00c3a5;'>Critical Touchpoints Analysis</h2>", unsafe_allow_html=True)

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

    # Create sentiment_classification column
    df['sentiment_classification'] = pd.cut(df['cleaned_sentiment'], 
                                            bins=[-1, -0.1, 0.1, 1], 
                                            labels=['Negative', 'Neutral', 'Positive'])

    # Function to create progress columns
    def create_progress_column(dataframe, column_name):
        max_value = dataframe[column_name].sum()
        percentage = dataframe[column_name].apply(lambda x: (x / max_value) * 100)
        cumulative = dataframe[column_name].cumsum().apply(lambda x: (x / max_value) * 100)
        return percentage, cumulative

    # Function to calculate weekly averages and coefficient of variation for each category
    def calculate_weekly_stats(df, category_column):
        df['week'] = pd.to_datetime(df['created_at']).dt.to_period('W')
        weekly_avg = df.groupby(['week', category_column])['cleaned_sentiment'].mean().unstack(fill_value=0)
        weekly_avg_list = weekly_avg.values.T.tolist()
        
        # Calculate coefficient of variation as a percentage
        cv = (weekly_avg.std() / weekly_avg.abs().mean()) * 100
        cv_list = cv.tolist()
        
        return weekly_avg_list, cv_list

    # Function to interpret Coefficient of Variation
    def interpret_cv(cv):
        if cv < 15:
            return "Low variability"
        elif 15 <= cv < 30:
            return "Moderate variability"
        else:
            return "High variability"

    # Calculate weekly averages and CV for categories
    weekly_averages, cv_list = calculate_weekly_stats(df, 'category_bert')

    # Create a single column for Critical Touchpoints Analysis
    category_counts_bert = df['category_bert'].value_counts().reset_index()
    category_counts_bert.columns = ['Touchpoint', 'Count']
    category_counts_bert['Touchpoint'] = category_counts_bert['Touchpoint'].astype(str)
    category_counts_bert['Percentage'], category_counts_bert['Cumulative'] = create_progress_column(category_counts_bert, 'Count')
    
    # Add Rank column
    category_counts_bert['Rank'] = range(1, len(category_counts_bert) + 1)
    
    # Add Weekly Average Sentiment, Coefficient of Variation, and CV Interpretation columns
    category_counts_bert['Weekly Average Sentiment'] = weekly_averages
    category_counts_bert['Coefficient of Variation'] = cv_list
    category_counts_bert['CV Interpretation'] = category_counts_bert['Coefficient of Variation'].apply(interpret_cv)

    # Calculate average sentiment for each category
    category_avg_sentiment = df.groupby('category_bert')['cleaned_sentiment'].mean()

    # Add Avg Sentiment column to category_counts_bert
    category_counts_bert['Avg Sentiment'] = category_counts_bert['Touchpoint'].map(category_avg_sentiment)

    # Reorder columns, moving 'Rank' to the first position
    category_counts_bert = category_counts_bert[['Rank', 'Touchpoint', 'Count', 'Percentage', 'Cumulative', 'Avg Sentiment', 'Weekly Average Sentiment', 'Coefficient of Variation', 'CV Interpretation']]

    # Create filters
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        selected_country_name = st.selectbox("Select a country", country_options, index=0)

    with col2:
        selected_sentiments = st.multiselect(
            "Select Sentiments",
            options=['Positive', 'Neutral', 'Negative'],
            default=[]
        )

    with col3:
        selected_urgency = st.multiselect(
            "Select Urgency Level",
            options=sorted(df['urgency_level'].unique()),
            default=[]
        )

    with col4:
        selected_cv_interpretation = st.multiselect(
            "Select CV Interpretation",
            options=['Low variability', 'Moderate variability', 'High variability'],
            default=[]
        )


    # Apply filters
    filtered_df = df.copy()
    if selected_country_name != 'All':
        filtered_df = filtered_df[filtered_df['country_name'] == selected_country_name]
    if selected_sentiments:
        filtered_df = filtered_df[filtered_df['sentiment_classification'].isin(selected_sentiments)]
    if selected_urgency:
        filtered_df = filtered_df[filtered_df['urgency_level'].isin(selected_urgency)]

    # Recalculate category_counts_bert based on filtered data
    category_counts_bert = filtered_df['category_bert'].value_counts().reset_index()
    category_counts_bert.columns = ['Touchpoint', 'Count']
    category_counts_bert['Touchpoint'] = category_counts_bert['Touchpoint'].astype(str)
    category_counts_bert['Percentage'], category_counts_bert['Cumulative'] = create_progress_column(category_counts_bert, 'Count')
    category_counts_bert['Rank'] = range(1, len(category_counts_bert) + 1)

    # Recalculate weekly averages and CV for categories
    weekly_averages, cv_list = calculate_weekly_stats(filtered_df, 'category_bert')
    category_counts_bert['Weekly Average Sentiment'] = weekly_averages
    category_counts_bert['Coefficient of Variation'] = cv_list
    category_counts_bert['CV Interpretation'] = category_counts_bert['Coefficient of Variation'].apply(interpret_cv)

    # Calculate average sentiment for each category
    category_avg_sentiment = filtered_df.groupby('category_bert')['cleaned_sentiment'].mean()

    # Add Avg Sentiment column to category_counts_bert
    category_counts_bert['Avg Sentiment'] = category_counts_bert['Touchpoint'].map(category_avg_sentiment)

    # Reorder columns, ensuring 'Rank' is first
    category_counts_bert = category_counts_bert[['Rank', 'Touchpoint', 'Count', 'Percentage', 'Cumulative', 'Avg Sentiment', 'Weekly Average Sentiment', 'Coefficient of Variation', 'CV Interpretation']]

    # Filter category_counts_bert based on CV Interpretation if selected
    if selected_cv_interpretation:
        category_counts_bert = category_counts_bert[category_counts_bert['CV Interpretation'].isin(selected_cv_interpretation)]
        filtered_df = filtered_df[filtered_df['category_bert'].isin(category_counts_bert['Touchpoint'])]

    # Recalculate metrics based on final filtered data
    total_reviews = int(filtered_df.shape[0])
    average_sentiment = float(filtered_df['cleaned_sentiment'].mean())
    high_urgency_percentage = float((filtered_df['urgency_level'] == 'High').mean() * 100)
    positive_percentage = float((filtered_df['sentiment_classification'] == 'Positive').mean() * 100)
    negative_percentage = float((filtered_df['sentiment_classification'] == 'Negative').mean() * 100)
    neutral_percentage = float((filtered_df['sentiment_classification'] == 'Neutral').mean() * 100)

    # Display KPIs
    st.markdown("---")  # Linha horizontal antes dos KPIs
    
    kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)
    
    with kpi1:
        st.metric("Total Reviews", f"{total_reviews:,}")
    with kpi2:
        st.metric("Avg Sentiment (-1 to 1)", f"{average_sentiment:.2f}")
    with kpi3:
        st.metric("High Urgency Cases", f"{high_urgency_percentage:.1f}%")
    with kpi4:
        st.metric("Positive Sentiment", f"{positive_percentage:.1f}%")
    with kpi5:
        st.metric("Negative Sentiment", f"{negative_percentage:.1f}%")
    with kpi6:
        st.metric("Neutral Sentiment", f"{neutral_percentage:.1f}%")
    
    st.markdown("---")  # Linha horizontal após os KPIs

    # Display the filtered dataframe
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
            "Avg Sentiment": st.column_config.NumberColumn(
                "Avg Sentiment (-1 to 1)",
                format="%.2f"
            ),
            "Weekly Average Sentiment": st.column_config.AreaChartColumn(
                "Weekly Average Sentiment",
                width="medium",
                help="Weekly average sentiment for each touchpoint over time",
                y_min=-1,
                y_max=1
            ),
            "Coefficient of Variation": st.column_config.NumberColumn(
                "Coefficient of Variation (%)",
                format="%.2f%%"
            ),
            "CV Interpretation": st.column_config.TextColumn(
                "CV Interpretation",
                help="Interpretation of the Coefficient of Variation"
            ),
        },
        hide_index=True,
        use_container_width=True
    )

    st.markdown("---")

    # Display the detailed filtered dataframe
    st.dataframe(
        filtered_df[[
            'content_en', 
            'cleaned_sentiment', 
            'sentiment_classification', 
            'category_bert', 
            'urgency_level',
            'issue_type',
            'created_at',
            'resolution_suggestion'
        ]],
        column_config={
            "content_en": st.column_config.TextColumn("English Content"),
            "cleaned_sentiment": st.column_config.NumberColumn("Sentiment Score", format="%.4f"),
            "sentiment_classification": st.column_config.TextColumn("Sentiment"),
            "category_bert": st.column_config.TextColumn("Touchpoint Category"),
            "urgency_level": st.column_config.TextColumn("Urgency Level"),
            "issue_type": st.column_config.TextColumn("Issue Type"),
            "created_at": st.column_config.DatetimeColumn("Date", format="DD/MM/YYYY"),
            "resolution_suggestion": st.column_config.TextColumn("Resolution Suggestion")
        },
        hide_index=True,
        use_container_width=True,
        height=400  # Você pode ajustar a altura conforme necessário
    )

    # End of the function
