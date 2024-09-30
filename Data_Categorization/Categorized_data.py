import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def display_categorized_data(df, country_options, country_mapping):
    st.header('Feedback Source Analysis')
    st.markdown("<hr style='border: 1px solid #00c3a5;'>",
                unsafe_allow_html=True)
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
        filtered_df['year_week'] = filtered_df['created_at'].dt.strftime(
            '%Y-%U')
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

        st.pyplot(fig)

        st.write("### Interpreting the Feedback Source Analysis")

        with st.expander("See explanation"):
            st.write("""
            1. **Distribution Tables (Right)**:
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

        st.markdown(
            "<p style='font-size: 1rem;'>Feedback Source Distribution</p>", unsafe_allow_html=True)

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

        st.markdown(
            "<p style='font-size: 1rem;'>Feedback Source Distribution by Country</p>", unsafe_allow_html=True)

        country_distribution = filtered_df.groupby(
            ['country_code', 'type']).size().unstack(fill_value=0)
        country_distribution_pct = country_distribution.div(
            country_distribution.sum(axis=1), axis=0) * 100

        country_distribution_pct.index = country_distribution_pct.index.map(
            country_mapping)

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

    st.write("___")  # Linha de separação

    st.header('Data Categorization')
    st.markdown("<h3 style='color: #00c3a5;'>This section provides an overview of the categorization process.</h3>",
                unsafe_allow_html=True)

    st.markdown("""
    The categorization process outlined below is structured into <span style='color: #00c3a5;'>8 distinct levels</span> of analysis. At the <span style='color: #00c3a5;'>first</span> level, all received feedback is grouped together, forming the primary dataset. Moving to the <span style='color: #00c3a5;'>second</span> level, this feedback is segmented by country. At the <span style='color: #00c3a5;'>third</span> level, within each country, the feedback is sorted into three categories: positive, neutral, and negative. The <span style='color: #00c3a5;'>fourth</span> level focuses on negative feedback, which is prioritized in the context of "Patient Care." This feedback is further broken down by medical practice areas, specifically highlighting three key areas in this example: Clinical Medicine, Surgery, and Mental Health.

    At the <span style='color: #00c3a5;'>fifth</span> level, I delve deeper within each practice area to include medical specialties, such as Cardiology and Endocrinology within the Clinical Medicine group. This approach by specialty aims to identify behavioral patterns within professional groups, enabling the development of broad-scale solutions.

    Moving to the <span style='color: #00c3a5;'>sixth</span> level, I focus on the process touchpoints, particularly within the Mental Health area in this example, highlighting the 11 touchpoints in the patient journey and identifying specific opportunities for operational improvement at DocPlanner. The <span style='color: #00c3a5;'>seventh</span> level assesses interactions based on three levels of urgency: low, medium, and high. Finally, at the <span style='color: #00c3a5;'>eighth</span> level, within the high-urgency category, I consider the limited capacity for action but with strong influence; through this "mass strategy," it is possible to enhance positive persuasion and drive improvements in medical best practices using real data from DocPlanner, thus completing the analysis framework and providing a strategic overview of the operation.

    In this context, "mass solutions" refers to implementing targeted interventions for large groups of professionals within a medical specialty. Since these solutions are designed to address recurring behaviors, their impact is magnified, leading to significant improvements in patient experience and increased engagement on the platform.
    """, unsafe_allow_html=True)

    st.write("___")  # Linha de separação

    st.markdown(
        "Below is a tree diagram that visually breaks down the categories for a clearer representation.")

    # Add the code block here
    st.code('''
1. Total Reviews/
├── 1.1 Country/
│   ├── 1.1.1 Sentiment/
│   │   ├── 1.1.1.1 Positive
│   │   ├── 1.1.1.2 Neutral
│   │   └── 1.1.1.3 Negative/
│   │       ├── 1.1.1.3.1 Practice Area/
│   │       │   ├── 1.1.1.3.1.1 Clinical Medicine/
│   │       │   │   ├── 1.1.1.3.1.1.1 Cardiologist
│   │       │   │   ├── 1.1.1.3.1.1.2 Endocrinologist
│   │       │   │   ├── 1.1.1.3.1.1.3 Gastroenterologist
│   │       │   │   └── 1.1.1.3.1.1.4 Pulmonologist
│   │       │   ├── 1.1.1.3.1.2 Surgery/
│   │       │   │   ├── 1.1.1.3.1.2.1 General Surgeon
│   │       │   │   ├── 1.1.1.3.1.2.2 Plastic Surgeon
│   │       │   │   └── 1.1.1.3.1.2.3 Orthopedist
│   │       │   ├── 1.1.1.3.1.3 Mental Health/
│   │       │   │   ├── 1.1.1.3.1.3.1 Psychologist
│   │       │   │   └── 1.1.1.3.1.3.2 Psychiatrist/
│   │       │   │       └── 1.1.1.3.1.3.2.1 Touchpoints/
│   │       │   │           ├── 1.1.1.3.1.3.2.1.1 Search and Evaluate Professional Score
│   │       │   │           ├── 1.1.1.3.1.3.2.1.2 Schedule Appointment
│   │       │   │           ├── 1.1.1.3.1.3.2.1.3 Make Payment Online
│   │       │   │           ├── 1.1.1.3.1.3.2.1.4 Make Payment at Reception
│   │       │   │           ├── 1.1.1.3.1.3.2.1.5 Check-in Online
│   │       │   │           ├── 1.1.1.3.1.3.2.1.6 Check-in at Reception
│   │       │   │           ├── 1.1.1.3.1.3.2.1.7 Attend Online Consultation
│   │       │   │           ├── 1.1.1.3.1.3.2.1.8 Attend Offline Consultation/
│   │       │   │           │   └── 1.1.1.3.1.3.2.1.8.1 Urgency Levels/
│   │       │   │           │       ├── 1.1.1.3.1.3.2.1.8.1.1 Low
│   │       │   │           │       ├── 1.1.1.3.1.3.2.1.8.1.2 Medium
│   │       │   │           │       ├── 1.1.1.3.1.3.2.1.8.1.3 High/
│   │       │   │           │       │   └── 1.1.1.3.1.3.2.1.8.1.3.1 🚫 Influence without autonomy to act 
│   │       │   │           ├── 1.1.1.3.1.3.2.1.9 Follow-up Procedures (e.g., Exams, Surgery)
│   │       │   │           └── 1.1.1.3.1.3.2.1.10 Leave Review and Feedback
    ''', language='text')

    st.markdown("In the next section, <span style='color: #00c3a5;'><strong>Critical Points Analysis</strong></span>, accessible from the sidebar on your left (⬅️), you'll gain deeper insights into how the touchpoints of the process were developed and mapped, providing a comprehensive understanding of their role within the overall framework.", unsafe_allow_html=True)

    st.markdown("<hr style='border: 1px solid #00c3a5;'>",
                unsafe_allow_html=True)
    col1, col2 = st.columns(2)
