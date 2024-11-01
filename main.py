import streamlit as st
from chatbot import bot_page
from file_loader import file_page
from myfunctions import start_recording, stop_recording
# Set up the Streamlit page
st.set_page_config(page_title="RAGBot", layout="wide")

# Default Page
if 'page' not in st.session_state:
    st.session_state['page'] = "Chatbot"

# Initialize chat sessions
if 'chat_sessions' not in st.session_state:
    st.session_state['chat_sessions'] = []  # List of all chat sessions
if 'current_chat' not in st.session_state:
    st.session_state['current_chat'] = None  # Track current active chat
if 'chat_counter' not in st.session_state:
    st.session_state['chat_counter'] = 1

# Sidebar 
with st.sidebar:
    st.title("Navigation")
    
    if st.button("New Chat", help="Create a new chat session"):
        # Create a new chat session
        new_chat_id = st.session_state['chat_counter']
        st.session_state['chat_sessions'].append(f"Chat {new_chat_id}")
        st.session_state['current_chat'] = f"Chat {new_chat_id}"
        st.session_state['page'] = "Chatbot"  # Ensure the page switches to the new chat
        st.session_state['chat_counter'] += 1  # Increment the counter for the next chat
    
    # Navigation for file loading
    if st.button("Load File", help="Upload your own files"):
        st.session_state['page'] = "Load File"

    st.write("---")
    if st.session_state['current_chat']:
        # Audio Input section
        st.write("## Record your question:")
        col1, col2 = st.columns([0.5, 0.5])
        col1.button('▶', on_click=start_recording, help="Start Recording")
        col2.button('🔴', on_click=stop_recording, help="Stop Recording")
        st.write("---")
    
    
    # Display buttons for each chat session
    st.write("## Select Chat")
    for chat in st.session_state['chat_sessions']:
        col1, col2 = st.columns([0.7, 0.3])  # Create two columns
        with col1:
            if st.button(chat):
                st.session_state['current_chat'] = chat
                st.session_state['page'] = "Chatbot"  # Switch to chatbot page when a chat is selected
        with col2:
            if st.button("🗑️", key=f"delete_{chat}"):  # Unique key for each delete button
                st.session_state['chat_sessions'].remove(chat)
                # Check if the deleted chat was the active one
                if st.session_state['current_chat'] == chat:
                    # Set current chat to None or the first available chat
                    if st.session_state['chat_sessions']:
                        st.session_state['current_chat'] = st.session_state['chat_sessions'][0]  # Set to first available chat
                    else:
                        st.session_state['current_chat'] = None  # No chats available

                st.rerun()  # Refresh the page to reflect changes

    st.write("---")
    

        
# Navigation based on selected page
if st.session_state['page'] == "Chatbot":
    bot_page()
elif st.session_state['page'] == "Load File":
    file_page()
