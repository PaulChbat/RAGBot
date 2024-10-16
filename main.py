# This file handles app config and page navigation 
import streamlit as st
from chatbot import bot_page
from file_loader import file_page
#from cost import cost_page
# Set up the Streamlit page
st.set_page_config(page_title="RAGBot", layout="wide")

# Sidebar navigation
# Default to the Chatbot page
if 'page' not in st.session_state:
    st.session_state['page'] = "Chatbot"
    
# Initialize session state for recording
if 'recording' not in st.session_state:
    st.session_state['recording'] = False
    st.session_state['frames'] = []  # To store audio frames

with st.sidebar:
    st.title("Navigation")
    if st.button("Chatbot"):
        st.session_state['page'] = "Chatbot"
    if st.button("Load File", help="Upload your own files"):
        st.session_state['page'] = "Load File"
    st.write("---")
    if st.session_state['page'] == "Chatbot":
        if st.button("New Chat", help="Start a new conversation"):
           st.session_state.messages = []

# Navigation based on page selection
if st.session_state['page'] == "Chatbot":
    bot_page()
elif st.session_state['page'] == "Load File":
    file_page()
