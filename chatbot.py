import streamlit as st
from myfunctions import get_answer

def bot_page():
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
            response = get_answer(vectorstore, query)
        else:
            response = f"No file is uploaded so I will act as an echo, you said: {query}"

        st.session_state.messages.append({"role": "assistant", "content": response})

    if st.session_state.messages:
        last_bot_message = st.session_state.messages[-1]
        last_user_message = st.session_state.messages[-2]
        st.chat_message("user").markdown(last_user_message["content"])
        st.chat_message("assistant").markdown(last_bot_message["content"])
