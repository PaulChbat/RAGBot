import streamlit as st
import os
from pathlib import Path
from myfunctions import get_answer, text_to_speech, start_recording, stop_recording, get_audio_query

def bot_page():
    st.title("RAGBot")

    # Ensure current chat is selected
    if st.session_state['current_chat'] is None:
        st.write("No chat selected. Please select or create a new chat session from the sidebar.")
        return

    # Initialize chat history for the selected session
    if st.session_state['current_chat'] not in st.session_state:
        st.session_state[st.session_state['current_chat']] = []

    # Create folder for the current chat session
    current_chat_folder = f"Audio/{st.session_state['current_chat']}"
    Path(current_chat_folder).mkdir(parents=True, exist_ok=True)

    # Display recording buttons in the sidebar
    with st.sidebar:
        st.write("Record your question:")
        col1, col2 = st.columns([0.5, 0.5])
        col1.button('▶', on_click=start_recording, help="Start Recording")
        col2.button('🔴', on_click=stop_recording, help="Stop Recording")

    # Get audio query if available
    audio_query = get_audio_query()
    
    # Text input for user query
    text_query = st.chat_input("Your Message...")

    query = text_query if text_query else audio_query

    if query:
        st.session_state[st.session_state['current_chat']].append({"role": "user", "content": query})
        
        # Generate the response
        if 'vectorstore' in st.session_state:
            vectorstore = st.session_state['vectorstore']
            response = get_answer(vectorstore, query)
        else:
            response = f"No file is uploaded, so I will act as an echo: {query}"
        
        # Append bot's response
        st.session_state[st.session_state['current_chat']].append({"role": "assistant", "content": response})

        # Convert response to speech and save it in the current chat folder
        audio_path = os.path.join(current_chat_folder, "response.mp3")
        text_to_speech(response, audio_path)

    # Display chat messages for the current session
    if st.session_state[st.session_state['current_chat']]:
        for message in st.session_state[st.session_state['current_chat']]:
            if message["role"] == "user":
                st.chat_message("user").markdown(message["content"])
            else:
                st.chat_message("assistant").markdown(message["content"])

    # Play the bot's response audio from the current chat folder
    audio_file = os.path.join(current_chat_folder, "response.mp3")
    if os.path.exists(audio_file) and st.session_state[st.session_state['current_chat']]:
        st.audio(audio_file)
