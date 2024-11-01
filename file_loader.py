# This file handles the File Upload Page 
import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from myfunctions import setup_vdb, show_content, show_chunks, save_load_files, show_files_in_database

def file_page():
    st.title("Load your File")
    uploaded_files = st.file_uploader("", type=["pdf", "docx", "xlsx"], accept_multiple_files=True)
    used_model_name = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    if uploaded_files:
        for uploaded_file in uploaded_files:
            st.success(f"File uploaded: {uploaded_file.name}")
        documents = save_load_files(uploaded_files)
        # Display the content of all the files
        show_content(documents)
        # Chunk the content
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)
        # Display the generated chunks
        show_chunks(texts)
        # Setup and save vectore DataBase
        setup_vdb(used_model_name,texts)

    st.write("---")
    option = st.selectbox(
        "Choose a Database to load:",
        ["Select an option...","USEK", "EXEO"]
    )
    if st.button("Load"):
        if option=="USEK":
            embeddings = HuggingFaceEmbeddings(model_name = used_model_name)
            try:
                vectorstore = FAISS.load_local('db_faiss_usek', embeddings, allow_dangerous_deserialization=True)
                st.session_state['vectorstore'] = vectorstore
                st.success("USEK DB loaded successfully!")
    
                # Show metadata (source filenames and page numbers) for the documents in the vectorstore
                if 'vectorstore' in st.session_state:
                    show_files_in_database(st.session_state['vectorstore'])
    
            except FileNotFoundError:
                st.error("No saved USEK DB found!")
        elif option=="EXEO":
            embeddings = HuggingFaceEmbeddings(model_name = used_model_name)
            try:
                vectorstore = FAISS.load_local('db_faiss_exeo', embeddings, allow_dangerous_deserialization=True)
                st.session_state['vectorstore'] = vectorstore
                st.success("EXEO DB loaded successfully!")
    
                # Show metadata (source filenames and page numbers) for the documents in the vectorstore
                if 'vectorstore' in st.session_state:
                    show_files_in_database(st.session_state['vectorstore'])
    
            except FileNotFoundError:
                st.error("No saved EXEO DB found!")
    
    #col1 ,col2 = st.columns(2)
    #with col1:
    #    if st.button("Load USEK Data"):
    #        embeddings = HuggingFaceEmbeddings(model_name = used_model_name)
    #        try:
    #            vectorstore = FAISS.load_local('db_faiss_usek', embeddings, allow_dangerous_deserialization=True)
    #            st.session_state['vectorstore'] = vectorstore
    #            st.success("USEK DB loaded successfully!")
#
    #            # Show metadata (source filenames and page numbers) for the documents in the vectorstore
    #            if 'vectorstore' in st.session_state:
    #                show_files_in_database(st.session_state['vectorstore'])
#
    #        except FileNotFoundError:
    #            st.error("No saved USEK DB found!")
    #with col2:
    #    if st.button("Load EXEO Data"):
    #        embeddings = HuggingFaceEmbeddings(model_name = used_model_name)
    #        try:
    #            vectorstore = FAISS.load_local('db_faiss_exeo', embeddings, allow_dangerous_deserialization=True)
    #            st.session_state['vectorstore'] = vectorstore
    #            st.success("EXEO DB loaded successfully!")
#
    #            # Show metadata (source filenames and page numbers) for the documents in the vectorstore
    #            if 'vectorstore' in st.session_state:
    #                show_files_in_database(st.session_state['vectorstore'])
#
    #        except FileNotFoundError:
    #            st.error("No saved EXEO DB found!")
#
