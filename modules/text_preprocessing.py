import re
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from modules.config import config
def clean_text(text: str) -> str:
    """
    Clean and normalize extracted website text.
    """
    text = text.replace("\t", " ")
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\x00-\x7F]+", " ", text)  # remove non-ascii
    return text.strip()


def get_text_splitter() -> RecursiveCharacterTextSplitter:
    """
    Returns configured LangChain text splitter.
    """
    return RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", " ", ""]
    )

def create_documents(
    cleaned_text: str,
    source_url: str,
    page_title: str = "Website Content"
) -> List[Document]:
    """
    Convert cleaned text into LangChain Documents with metadata.
    """
    splitter = get_text_splitter()

    documents = splitter.create_documents(
        texts=[cleaned_text],
        metadatas=[{
            "source": source_url,
            "title": page_title
        }]
    )

    return documents

#ye full processing pipeline hai
def process_website_text(
    raw_text: str,
    source_url: str,
    page_title: str = "Website Content"
) -> List[Document]:
    """
    Complete text processing pipeline.
    """
    cleaned_text = clean_text(raw_text)

    if not cleaned_text:
        return []

    documents = create_documents(
        cleaned_text=cleaned_text,
        source_url=source_url,
        page_title=page_title
    )

    return documents


#print(process_website_text("Hello world! This is a sample text to demonstrate the text processing pipeline.", "https://openrouter.ai/openai/gpt-oss-120b:free", "Sample Page"))  # Example usage