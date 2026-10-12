import Stemmer
from llama_index.core.indices.document_summary import (
    DocumentSummaryIndexEmbeddingRetriever,
    DocumentSummaryIndexLLMRetriever,
)
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.retrievers.bm25 import BM25Retriever

from shared import (
    build_nodes, build_summary_index, build_vector_index, configure_models,
    load_documents, show_results,
)


def vector_index_retriever(vector_index):
    retriever = VectorIndexRetriever(index=vector_index, similarity_top_k=3)

    query = "What is machine learning?"
    print(f"Query: {query}\n")
    show_results(retriever.retrieve(query))


def bm25_retriever(nodes):
    retriever = BM25Retriever.from_defaults(
        nodes=nodes,
        similarity_top_k=3,
        stemmer=Stemmer.Stemmer("english"),  # normalizes word forms, so "networks" matches "network"
        language="english",
    )

    query = "neural networks deep learning"
    print(f"Query: {query}\n")
    show_results(retriever.retrieve(query))


def document_summary_index_retriever(summary_index):
    llm_retriever = DocumentSummaryIndexLLMRetriever(summary_index, choice_top_k=3)
    embedding_retriever = DocumentSummaryIndexEmbeddingRetriever(summary_index, similarity_top_k=3)

    query = "different types of learning"
    print(f"Query: {query}\n")

    show_results(llm_retriever.retrieve(query))

    print("\nEmbedding-based:")
    show_results(embedding_retriever.retrieve(query))


def main():
    configure_models()
    documents = load_documents()
    nodes = build_nodes(documents)

    vector_index_retriever(build_vector_index(documents))
    bm25_retriever(nodes)
