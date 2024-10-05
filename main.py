import streamlit as st
from chatbot import bot_page
from file_loader import file_page
from cost import cost_page

# Set up the Streamlit page
st.set_page_config(page_title="RAGBot", layout="wide")

# Sidebar navigation
with st.sidebar:
    st.title("Navigation")
    if st.button("Chatbot"):
        st.session_state['page'] = "Chatbot"
    if st.button("Load File"):
        st.session_state['page'] = "Load File"
    if st.button("Cost"):
        st.session_state['page'] = "Cost"

# Default to the Chatbot page
if 'page' not in st.session_state:
    st.session_state['page'] = "Chatbot"

# Navigation based on page selection
if st.session_state['page'] == "Chatbot":
    bot_page()
elif st.session_state['page'] == "Load File":
    file_page()
elif st.session_state['page'] == "Cost":
    cost_page()
