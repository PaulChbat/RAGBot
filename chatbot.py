import streamlit as st
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def bot_page():
    st.title("RAGBot")
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # React to user input
    if prompt := st.chat_input("Your Message..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Generate the response
        if 'vectorstore' in st.session_state:
            vectorstore = st.session_state['vectorstore']
            full_response_with_scores = vectorstore.similarity_search_with_score(prompt)

            if len(full_response_with_scores) > 0:
                top_3_responses = full_response_with_scores[:3]
                response = ""
                for i, (chunk, score) in enumerate(top_3_responses, 1):
                    if chunk.metadata['source'].split('.')[-1].lower() == "pdf":
                        response += f"Chunk {i} : {score:.4f} | Source: {chunk.metadata['source']} | Page: {chunk.metadata['page']} \n\n{chunk.page_content}\n\n"
                    else:    
                        response += f"Chunk {i} : {score:.4f} | Source: {chunk.metadata['source']} \n\n{chunk.page_content}\n\n"
            else:
                response = "No relevant information found."
        else:
            response = f"No file is uploaded so I will act as an echo, you said: {prompt}"

        st.session_state.messages.append({"role": "assistant", "content": response})

    if st.session_state.messages:
        last_bot_message = st.session_state.messages[-1]
        last_user_message = st.session_state.messages[-2]
        st.chat_message("user").markdown(last_user_message["content"])
        st.chat_message("assistant").markdown(last_bot_message["content"])
