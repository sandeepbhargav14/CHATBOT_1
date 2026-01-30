import os
from typing import List
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
import shutil
from modules.embeddings import get_embedding_model
from modules.config import config
def clear_vector_store():
    """
    Delete existing FAISS vector database.
    """
    if os.path.exists(config.VECTOR_DB_PATH):
        shutil.rmtree(config.VECTOR_DB_PATH)

def create_vector_store(documents: List[Document]) -> FAISS:
    """
    Create FAISS vector store from documents and persist to disk.
    """
    embedding_model = get_embedding_model()

    vector_store = FAISS.from_documents(
        documents=documents,
        embedding=embedding_model
    )

    os.makedirs(config.VECTOR_DB_PATH, exist_ok=True)
    vector_store.save_local(config.VECTOR_DB_PATH)

    return vector_store


def load_vector_store():
    """
    Load vector store only if FAISS index exists.
    """
    index_file = os.path.join(config.VECTOR_DB_PATH, "index.faiss")

    if not os.path.exists(index_file):
        return None

    embedding_model = get_embedding_model()

    return FAISS.load_local(
        config.VECTOR_DB_PATH,
        embeddings=embedding_model,
        allow_dangerous_deserialization=True
    )


def get_or_create_vector_store(documents: List[Document]) -> FAISS:
    """
    Load existing vector DB or create new one.
    """
    vector_store = load_vector_store()

    if vector_store:
        return vector_store

    return create_vector_store(documents)
