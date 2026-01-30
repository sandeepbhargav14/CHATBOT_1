import streamlit as st
from modules.config import config
from modules.url_validator import validate_url
from modules.crawel import crawl_website
from modules.text_preprocessing import process_website_text
from modules.vector_store import get_or_create_vector_store
from modules.qa_chain import build_qa_chain, get_answer,build_conversational_qa_chain
from modules.vector_store import clear_vector_store

from dotenv import load_dotenv
load_dotenv()
# ------------------ PAGE SETUP ------------------
st.set_page_config(page_title=config.APP_NAME)
st.title(config.APP_NAME)

# ------------------ SESSION INIT ------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ------------------ URL INPUT ------------------
url = st.text_input("Enter Website URL")

# ------------------ INDEX WEBSITE ------------------
if st.button("Index Website"):
    if validate_url(url):
        clear_vector_store()
        
        with st.spinner("Crawling website..."):
            raw_content = crawl_website(url)

        if raw_content:
            with st.spinner("Processing & chunking text..."):
                documents = process_website_text(
                    raw_text=raw_content,
                    source_url=url
                )

            with st.spinner("Creating embeddings & vector database..."):
                vector_store = get_or_create_vector_store(documents)

            # ✅ SAVE IN SESSION
            st.session_state.vector_store = vector_store
            st.session_state.qa_chain = build_conversational_qa_chain(vector_store)
            st.session_state.chat_history = []

            st.success("Website indexed successfully. You can now chat with the website.")
        else:
            st.error("Content extraction failed.")
    else:
        st.error("Invalid or unreachable URL.")

# ------------------ CHAT UI ------------------
st.divider()
st.subheader("Chat with Website")

if "vector_store" in st.session_state:
    user_question = st.chat_input("Ask something about the website...")

    if user_question:
        with st.spinner("Thinking..."):
            result = st.session_state.qa_chain({
                "question": user_question,
                "chat_history": st.session_state.chat_history
            })

            answer = result["answer"]

        st.session_state.chat_history.append((user_question, answer))

    for q, a in st.session_state.chat_history:
        with st.chat_message("user"):
            st.write(q)
        with st.chat_message("assistant"):
            st.write(a)