# This file handles the chatbot page
import streamlit as st
import os
from myfunctions import get_answer, text_to_speech, transcribe_audio, start_recording, stop_recording, get_audio_query
from audio_recorder_streamlit import audio_recorder

def bot_page():
    st.title("RAGBot")
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Buttons to control recording 
    with st.sidebar:
        st.write("Record your question:")
        col1, col2 = st.columns([0.5,0.5])
        col1.button('▶', on_click=start_recording, help="Start Recording")
        col2.button('🔴', on_click=stop_recording, help="Stop Recording")
    # Fetch the transcribed audio input
    audio_query = get_audio_query()
    
    st.write("---")
    
    text_query = st.chat_input("Your Message...")
    if text_query:
        query = text_query # If there's a text query, use it
    elif audio_query:   
        query = audio_query # If there's no text query but audio was recorded, use the transcription
    else:
        query = None  # No input provided
    
    if query:
        st.session_state.messages.append({"role": "user", "content": query})
        
        # Generate the response
        if 'vectorstore' in st.session_state:
            vectorstore = st.session_state['vectorstore']
            response = get_answer(vectorstore, query)
            #st.session_state['cost'] += query_cost 
        else:
            response = f"No file is uploaded so I will act as an echo, you said: {query}"

        st.session_state.messages.append({"role": "assistant", "content": response})

        # Convert the bot's response to speech
        text_to_speech(response, "Audio/response.mp3")

    if st.session_state.messages:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.chat_message("user").markdown(message["content"])
            elif message["role"] == "assistant":
                st.chat_message("assistant").markdown(message["content"])

    
    # Add a button to play the response audio
    if os.path.exists("Audio/response.mp3") and st.session_state.messages:
        st.audio("Audio/response.mp3")  

    
        