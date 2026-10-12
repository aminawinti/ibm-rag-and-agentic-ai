import Stemmer
from llama_index.retrievers.bm25 import BM25Retriever

from shared import (
    build_nodes, build_vector_index, configure_models, load_documents,
)


def normalize(results):
    """Scale scores to [0, 1] by the best score, keyed by node text."""
    best = max((r.score for r in results), default=0) or 1.0  # `or 1.0` avoids dividing by zero when nothing matches
    return {r.text.strip(): r.score / best for r in results}


def hybrid_retrieve(query, vector_retriever, bm25_retriever, top_k=5, vector_weight=0.7, bm25_weight=0.3):
    vector_scores = normalize(vector_retriever.retrieve(query))
    bm25_scores = normalize(bm25_retriever.retrieve(query))

    ranked = [
        {
            "text": text,
            "vector": vector_scores.get(text, 0),
            "bm25": bm25_scores.get(text, 0),
            "hybrid": vector_weight * vector_scores.get(text, 0) + bm25_weight * bm25_scores.get(text, 0),
        }
        for text in set(vector_scores) | set(bm25_scores)
    ]
    return sorted(ranked, key=lambda r: r["hybrid"], reverse=True)[:top_k]


def main():
    configure_models()
    documents = load_documents()

    # top_k=10 = whole corpus, so both retrievers rank every document
    vector_retriever = build_vector_index(documents).as_retriever(similarity_top_k=10)
    bm25_retriever = BM25Retriever.from_defaults(
        nodes=build_nodes(documents),
        similarity_top_k=10,
        stemmer=Stemmer.Stemmer("english"),
        language="english",
    )

    test_queries = [
        "What is machine learning?",         # semantic
        "neural networks deep learning",     # keyword
        "supervised learning techniques",    # mixed
    ]

    for query in test_queries:
        print(f"Query: {query}")
        for rank, r in enumerate(hybrid_retrieve(query, vector_retriever, bm25_retriever, top_k=3), 1):
            print(f"{rank}. hybrid={r['hybrid']:.3f} (vector={r['vector']:.3f}, bm25={r['bm25']:.3f}) {r['text'][:70]}")
        print()


if __name__ == "__main__":
    main()
