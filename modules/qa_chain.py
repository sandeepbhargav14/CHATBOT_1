from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from modules.memory import get_session_memory
from modules.config import config
from dotenv import load_dotenv
load_dotenv()
QA_PROMPT = PromptTemplate(
    template="""
You are a website-based AI assistant.
Answer the question strictly using ONLY the context provided below.

Context:
{context}

Question:
{question}

Rules:
- Do NOT use external knowledge.
- Do NOT make assumptions.
- If the answer is NOT present in the context, respond EXACTLY with:
"The answer is not available on the provided website."
""",
    input_variables=["context", "question"]
)


def get_llm():
    """
    Load LLM model.
    """
    return ChatOpenAI(
        model_name=config.LLM_MODEL_NAME,
        temperature=0
    )
    
    
def build_qa_chain(vector_store: FAISS) -> RetrievalQA:
    """
    Create Retrieval QA chain using vector store.
    """
    llm = get_llm()

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=False,
        chain_type_kwargs={"prompt": QA_PROMPT}
    )

    return qa_chain


def get_answer(qa_chain: RetrievalQA, question: str) -> str:
    """
    Get answer from QA chain with fallback handling.
    """
    result = qa_chain.run(question)

    if not result or result.strip() == "":
        return "The answer is not available on the provided website."

    return result



def build_conversational_qa_chain(vector_store: FAISS):
    """
    Conversational QA chain with short-term memory.
    """
    llm = get_llm()
    memory = get_session_memory()

    retriever = vector_store.as_retriever(
        search_kwargs={"k": 4}
    )

    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": QA_PROMPT},
        return_source_documents=False
    )

    return qa_chain
