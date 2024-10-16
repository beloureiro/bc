import streamlit as st
import pandas as pd
from news_strategies import display_news_strategies  # Importando a função

def run_strategic_goals():
    st.markdown("<h1><span style='color: #00c3a5;'>Beyond the Scope:</span> Strategic Actions for Enhancing Patient Satisfaction, Engagement, and Expectation Management</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        After an extensive analysis of a dataset comprising approximately 50,000 customer reviews across three countries, 
        and considering the sentiment indicators tied to specific processes, I identified potential opportunities that extend beyond the initial scope of the business case. 
        As a result, I developed a strategic action plan aimed at supporting patient satisfaction, fostering loyalty, and potentially contributing to growth for DocPlanner.

        It's important to note that, due to the lack of direct validation with the DocPlanner team, some of the proposed actions might not align with the current strategies or may already be in place. However, I believe these suggestions could still offer value and serve as a starting point for further discussion and refinement.

        **I trust this additional insight will be valuable:)**
        """)
    with col2:
        st.markdown("""
        The strategic action plan is structured into 10 actions organized across 8 categories as follows:

        - <span style='color: #00c3a5;'>Expectation Management and Transparency</span> (EMT)
        - <span style='color: #00c3a5;'>Enhancing Patient Satisfaction Post-Consultation</span> (EPS)
        - <span style='color: #00c3a5;'>Direct Monetization</span> (DM)
        - <span style='color: #00c3a5;'>User Engagement</span> (UE)
        - <span style='color: #00c3a5;'>Partnerships and Service Expansion</span> (PSE)
        - <span style='color: #00c3a5;'>Platform and Tool Improvement</span> (PTI)
        - <span style='color: #00c3a5;'>Marketing and Communication</span> (MC)
        - <span style='color: #00c3a5;'>Data Analysis and Insights</span> (DAI)
        """, unsafe_allow_html=True)

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

    st.markdown("<h2 style='color: #00c3a5;'>Analysis of the Value Proposition</h2>", unsafe_allow_html=True)
    st.markdown("The current value proposition is:")
    st.markdown("""
    <div style='background-color: #262730; border-radius: 10px; padding: 20px; text-align: center; font-size: 24px;'>
        <strong>Patient get to know you <span style='color: #00c3a5; font-size: 26px;'>+</span> Patients get to trust you (opinions, online reputation) <span style='color: #00c3a5; font-size: 26px;'>=</span> Patients get to book with you</strong>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    **Flaws and Opportunities for Improvement:**

    - **Limited Focus on Pre-Consultation:** The value proposition concentrates only on the steps leading to booking, neglecting the patient's experience during and after the consultation.
    - **Unmanaged Expectations:** High ratings can create elevated expectations which, if unmet, lead to dissatisfaction and blame directed at both the doctor and DocPlanner.
    - **Shared Responsibility:** When expectations are not met, the platform is held accountable alongside the doctor, affecting its reputation and user trust.

    **Opportunities for Improvement:**

    - **Expand the Value Proposition:** Include elements that ensure patient satisfaction throughout the entire care cycle, not just up to the booking.
    - **Expectation Management:** Provide more detailed and accurate information about doctors' services and practices to align patient expectations.
    - **Post-Consultation Support:** Implement post-care support to handle possible dissatisfaction, preventing complaints directed at the platform.
    """)

    # Load the CSV data for actions
    actions_df = pd.read_csv("Knowledge_Center/actions_text.csv")

    # Display the dataframe
    st.write("### Actions and Opportunities")
    st.dataframe(actions_df)
    st.write("___")  # Linha de separação
    # Chamar a função para exibir as estratégias de notícias
    display_news_strategies()  # Invocando a função aqui
