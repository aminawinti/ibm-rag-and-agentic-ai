from llama_index.core import Document, DocumentSummaryIndex, Settings, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter

from config import (
    EMBED_MODEL, LLM_MODEL_ID, LLM_TEMPERATURE, PROJECT_ID, SAMPLE_DOCUMENTS, WATSONX_URL,
)

def configure_models():
    """ Register the LLM and embedding model on Settings and return the LLM. """
    # imported here so scripts that never touch the models still import cleanly
    from ibm_watsonx_ai import APIClient
    from llama_index.embeddings.huggingface import HuggingFaceEmbedding
    from llama_index.llms.ibm import WatsonxLLM

    llm = WatsonxLLM(
        model_id=LLM_MODEL_ID,
        url=WATSONX_URL,
        project_id=PROJECT_ID,
        api_client=APIClient({"url": WATSONX_URL}),
        temperature=LLM_TEMPERATURE,
    )

    # global variable
    Settings.llm = llm
    Settings.embed_model = HuggingFaceEmbedding(model_name=EMBED_MODEL)

    return llm

def load_documents():
    return [Document(text=text) for text in SAMPLE_DOCUMENTS]

def build_nodes(documents):
    # one node per document at this size
    return SentenceSplitter().get_nodes_from_documents(documents)

def build_vector_index(documents):
    return VectorStoreIndex.from_documents(documents)

def build_summary_index(documents):
    # the LLM writes one summary per document at indexing time
    return DocumentSummaryIndex.from_documents(documents)

def show_results(results, width=90):
    """Print retrieved nodes as: rank. [score] text"""
    for rank, result in enumerate(results, 1):
        score = f"{result.score:.4f}" if result.score is not None else "n/a"
        print(f"{rank}. [{score}] {result.text[:width]}")
