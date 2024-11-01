# RAGBot
RAGBot allows you to upload your own files, including PDF, Word, and Excel documents, and interact with an intelligent chatbot to ask questions directly related to the content.

# Features
- **Voice Recognition & Text-to-Speech:** Leverages Groq for speech recognition and Deepgram for text-to-speech capabilities, enabling seamless voice interaction.
- **Multiple Chat Sessions:** Create and manage multiple chat sessions, each maintaining its own distinct conversation history, with the option to delete any chat.
- **Document Interaction:** Upload various document formats (PDF, DOCX, XLSX) and ask the chatbot specific questions related to the uploaded files.

# Example Usage
In this example, with the use of web scraping, i ask the bot question about USEK.
![image](https://github.com/user-attachments/assets/76dc72c7-a959-4ad2-97b5-e20a78086937)

# Next Steps:
- **Performance Optimization:** Enhance the system's efficiency and speed to improve user experience.
- **Text-To-Speech** Use a library for TTS that allows more than 2000 characters as input.

# Current Issues:
- Any response > 2000 characters will generated an error from Deepgram (exceeding max text input), u can change chat and go back to your chat and the response will be shown, but without the valid audio.

