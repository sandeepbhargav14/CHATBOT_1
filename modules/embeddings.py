from langchain_community.embeddings import HuggingFaceEmbeddings
from modules.config import config


def get_embedding_model():
    """
    Load and return embedding model.
    """
    return HuggingFaceEmbeddings(
        model_name=config.EMBEDDING_MODEL
    )
