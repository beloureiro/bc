import streamlit as st
from .mermaid_full_lifecycle import full_lifecycle_sequence_diagram
from .mermaid_compact_lifecycle import compact_lifecycle_sequence_diagram

def toggle_diagram():
    if 'show_full_version' not in st.session_state:
        st.session_state.show_full_version = False  # Default to the compact version

    if st.session_state.show_full_version:
        if st.button("Show Compact Version"):
            st.session_state.show_full_version = False
            st.rerun()
    else:
        if st.button("Show Full Version"):
            st.session_state.show_full_version = True
            st.rerun()

    if st.session_state.show_full_version:
        full_lifecycle_sequence_diagram()
    else:
        compact_lifecycle_sequence_diagram()

# Call the toggle_diagram function to render the appropriate version
toggle_diagram()
