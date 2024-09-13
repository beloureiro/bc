import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker



def display_categorized_data(df, country_options, country_mapping):
    st.header('Feedback Source Analysis')
    st.markdown("""
    This section presents an analysis of feedback sources based on the dataset. The dataset categorizes feedback into five sources: case, opinion, CSAT, Promoter Ninja, and AppFollow.
    """)

    col1, col2 = st.columns(2)

    with col1:
        selected_country = st.selectbox(
            'Select Country for Feedback Source Analysis', country_options)

        if selected_country == 'All':
            filtered_df = df
        else:
            selected_country_code = list(country_mapping.keys())[list(
                country_mapping.values()).index(selected_country)]
            filtered_df = df[df['country_code'] == selected_country_code]

        filtered_df['created_at'] = pd.to_datetime(filtered_df['created_at'])
        filtered_df['year_week'] = filtered_df['created_at'].dt.strftime('%Y-%U')
        filtered_df['week'] = filtered_df['created_at'].dt.isocalendar().week

        weekly_data = filtered_df.groupby(
            ['week', 'type']).size().unstack(fill_value=0)

        fig, ax = plt.subplots(figsize=(10, 6))
        fig.patch.set_facecolor('#0e1117')
        ax.set_facecolor('#262730')

        weekly_data.plot(kind='area', stacked=True, ax=ax, colormap='Set3')

        ax.set_title('Weekly Feedback Type Distribution', color='white')
        ax.set_xlabel('Week of Year', color='white')
        ax.set_ylabel('Count', color='white')
        ax.tick_params(axis='x', colors='white', rotation=45)
        ax.tick_params(axis='y', colors='white')

        ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
        ax.set_xticklabels(weekly_data.index, rotation=45,
                        ha='right', color='white')

        legend = ax.legend(title="Feedback Type", loc="upper center", bbox_to_anchor=(
            0.5, -0.15), ncol=len(weekly_data.columns))
        legend.get_title().set_color('white')
        legend.set_frame_on(False)
        for text in legend.get_texts():
            text.set_color('white')

        st.write("### Feedback Type Analysis Across Weekly Intervals")
        st.pyplot(fig)

        st.write("### Interpreting the Feedback Source Analysis")

        with st.expander("See explanation"):
            st.write("""
            1. **Distribution Table (Right)**:
            - This table shows the count, percentage, and cumulative percentage of each feedback source.
            - The progress bars visually represent the percentage and cumulative percentage, making it easy to compare the prevalence of different feedback sources.
            - The Pareto principle can be observed through the cumulative percentage column.

            2. **Weekly Distribution Chart (Left)**:
            - This stacked area chart shows how the distribution of feedback sources varies over time.
            - Each color represents a different feedback source, and the height of each area shows its proportion within the week.
            - This visualization helps identify trends and patterns in feedback sources across weeks.

            3. **Country Distribution Table (Right)**:
            - This table shows how the distribution of feedback sources varies by country.
            - The progress bars represent the percentage of each feedback source within each country.
            - This visualization helps identify trends and patterns in feedback sources across countries.

            4. **Key Insights**:
            - Observe which feedback sources are most common in each country and how their proportions differ.
            - Look for any significant differences between countries or trends over time, which might indicate regional preferences or issues.

            5. **Implications**:
            - Understanding how feedback sources vary by country and over time can help tailor strategies for different regions and adapt to changing trends.
            - Countries or time periods with unusual distributions might require more focused attention or analysis.
            """)

    with col2:
        type_counts = filtered_df['type'].value_counts()
        type_percentages = filtered_df['type'].value_counts(
            normalize=True) * 100

        cumulative_percentage = type_percentages.cumsum()

        type_analysis = pd.DataFrame({
            'Count': type_counts,
            'Percentage': type_percentages,
            'Cumulative %': cumulative_percentage
        })
        
        type_analysis.index.name = "Source"

        st.markdown("### Feedback Source Distribution")

        st.dataframe(type_analysis.reset_index(), column_config={
            "Source": st.column_config.TextColumn("Source"),
            "Percentage": st.column_config.ProgressColumn(
                "Percentage (%)",
                help="This column shows the percentage of each feedback type",
                min_value=0,
                max_value=100,
                format="%.2f%%"
            ),
            "Cumulative %": st.column_config.ProgressColumn(
                "Cumulative %",
                help="This column shows the cumulative percentage (Pareto)",
                min_value=0,
                max_value=100,
                format="%.2f%%"
            )
        }, hide_index=True, use_container_width=True)

        st.write("### Feedback Source Distribution by Country")

        country_distribution = filtered_df.groupby(['country_code', 'type']).size().unstack(fill_value=0)
        country_distribution_pct = country_distribution.div(country_distribution.sum(axis=1), axis=0) * 100

        country_distribution_pct.index = country_distribution_pct.index.map(country_mapping)

        country_distribution_pct = country_distribution_pct.T

        country_distribution_pct.index.name = "Source"

        column_config = {
            "Source": st.column_config.TextColumn("Source"),
        }

        for country in country_distribution_pct.columns:
            column_config[country] = st.column_config.ProgressColumn(
                country,
                help=f"Percentage of feedback sources in {country}",
                format="%.2f%%",
                min_value=0,
                max_value=100,
            )

        st.data_editor(
            country_distribution_pct.reset_index(),
            column_config=column_config,
            hide_index=True,
            use_container_width=True,
        )

    st.header('2. Data Categorization - Structured Data Analysis')
    st.markdown("<h3 style='color: #00c3a5;'>This section will cover the structured data analysis process.</h3>",
                unsafe_allow_html=True)

