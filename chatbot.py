import streamlit as st
import os
from pathlib import Path
from myfunctions import get_answer, text_to_speech, get_audio_query

def bot_page():
    if st.session_state['current_chat']:
        st.title(f"RAGBot - {st.session_state['current_chat']}")
    else:
        st.title("RAGBot")

    # Ensure a chat ais selected, if not prompt the user to start a new one
    if st.session_state['current_chat'] is None:
        st.markdown(
            """
            ### No chat selected
            Please select or create a new chat session from the sidebar.

            ### **Tips:**
            - Avoid changing the subject within the same chat. Instead, open a new chat for each new topic or question.
            """
        )
        return

    # Initialize chat history for the selected session
    if st.session_state['current_chat'] not in st.session_state:
        st.session_state[st.session_state['current_chat']] = []

    # Create folder for the current chat session to save latest response audio
    current_chat_folder = f"Audio/{st.session_state['current_chat']}"
    Path(current_chat_folder).mkdir(parents=True, exist_ok=True)
        
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
            response = get_answer(vectorstore)
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
        st.audio(audio_file, autoplay = False)
