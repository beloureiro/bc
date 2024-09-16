import streamlit as st
import pandas as pd

def run_strategic_goals():
    st.title("Strategic Actions for Enhancing Patient Satisfaction and Engagement")
    st.markdown("""
    After an extensive analysis of a dataset comprising approximately 50,000 customer reviews across three countries, 
    and based on the sentiment indicator that considers specific processes, even though it may not be within the scope of the business case, 
    I took the liberty of developing a strategic action plan to enhance patient satisfaction, foster loyalty, and drive growth for DocPlanner. 
    The goal is to contribute to the company's growth in the market, increase user engagement, and uncover new revenue opportunities.

    **I hope this will be useful.**
    """)

    # Load the CSV data
    df = pd.read_csv("Knowledge_Center/Actions_strategic.csv")

    # Split the 'Revenue and Engagement Opportunities' column
    df['Revenue and Engagement Opportunities'] = df['Revenue and Engagement Opportunities'].fillna('')
    split_df = df['Revenue and Engagement Opportunities'].str.split('\n- ', expand=True)
    split_df.columns = ['Category_' + str(col) for col in split_df.columns]
    
    # Combine the original dataframe with the split categories
    df = pd.concat([df, split_df], axis=1)
    
    # Melt the dataframe to create separate rows for each category
    id_vars = ['Section', 'Category', 'Premise', 'Actions']
    value_vars = [col for col in df.columns if col.startswith('Category_')]
    melted_df = df.melt(id_vars=id_vars, value_vars=value_vars, var_name='Category_Number', value_name='Opportunity')
    
    # Remove rows with empty opportunities and reset index
    melted_df = melted_df[melted_df['Opportunity'].notna() & (melted_df['Opportunity'] != '')].reset_index(drop=True)

    # Create two columns
    col1, col2 = st.columns([2, 1])

    # Column 1: Text description
    description = """
    The strategic action plan is structured into 10 actions organized across 8 categories, each grounded in practical premises to facilitate effective management and implementation. The categories include:

    - Expectation Management and Transparency (EMT)
    - Enhancing Patient Satisfaction Post-Consultation (EPS)
    - Direct Monetization (DM)
    - User Engagement (UE)
    - Partnerships and Service Expansion (PSE)
    - Platform and Tool Improvement (PTI)
    - Marketing and Communication (MC)
    - Data Analysis and Insights (DAI)
    """
    col1.markdown(description)

    # Column 2: Filter buttons
    with col2:
        st.subheader("Filter by Action")
        sections = melted_df['Section'].unique().tolist()
        selected_sections = st.multiselect("Select actions:", sections)

    # Filter the dataframe based on selected sections
    if selected_sections:
        df_filtered = melted_df[melted_df['Section'].isin(selected_sections)]
    else:
        df_filtered = melted_df

    # Display the filtered dataframe without Section and Category columns
    st.dataframe(df_filtered.drop(columns=['Section', 'Category', 'Category_Number']))

