# This file handles the chatbot page
import streamlit as st
import os
from myfunctions import get_answer, text_to_speech

def bot_page():
    if 'cost' not in st.session_state:
        st.session_state['cost'] = 0

    st.title("RAGBot")
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # React to user input
    if query := st.chat_input("Your Message..."):
        st.session_state.messages.append({"role": "user", "content": query})
        
        # Generate the response
        if 'vectorstore' in st.session_state:
            vectorstore = st.session_state['vectorstore']
            response,query_cost = get_answer(vectorstore, query)
            st.session_state['cost'] += query_cost 
        else:
            response = f"No file is uploaded so I will act as an echo, you said: {query}"

        st.session_state.messages.append({"role": "assistant", "content": response})

        # Convert the bot's response to speech
        text_to_speech(response, "Audio/response.mp3")

    if st.session_state.messages:
        last_bot_message = st.session_state.messages[-1]
        last_user_message = st.session_state.messages[-2]
        st.chat_message("user").markdown(last_user_message["content"])
        st.chat_message("assistant").markdown(last_bot_message["content"])
    
    # Add a button to play the response audio
    if os.path.exists("Audio/response.mp3") and st.session_state.messages:
        if st.button("Play Response"):
            st.audio("Audio/response.mp3")