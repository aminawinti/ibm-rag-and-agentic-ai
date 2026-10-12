from llama_index.core.retrievers import QueryFusionRetriever

from shared import (
    build_vector_index, configure_models, load_documents, show_results,
)

# how scores are combined in each mode (verified against the llama-index source)
FUSION_MODES = {
    # sum of 1 / (rank + 60) over every list a node appears in. ignores raw
    # scores, so it is robust when lists use different scales (BM25 vs cosine)
    "reciprocal_rerank": "rank-based",

    # min-max scale each list to [0, 1], apply retriever weights, sum.
    # keeps the relative gaps between scores
    "relative_score": "min-max scaled",

    # same, but the scaling bounds are mean +/- 3 standard deviations instead
    # of the observed min and max. less sensitive to one outlier score
    "dist_based_score": "mean +/- 3 std scaled",
}


def run_fusion(vector_index, query):
    base_retriever = vector_index.as_retriever(similarity_top_k=5)

    for mode, description in FUSION_MODES.items():
        retriever = QueryFusionRetriever(
            [base_retriever],
            similarity_top_k=3,
            num_queries=3,
            mode=mode,
            use_async=False,
            verbose=True,  # prints the LLM-generated query variations
        )
        print(f"\n--- {mode} ({description}) ---")
        show_results(retriever.retrieve(query))


def main():
    configure_models()
    vector_index = build_vector_index(load_documents())

    query = "What are the main approaches to machine learning?"
    print(f"Query: {query}")
    run_fusion(vector_index, query)


if __name__ == "__main__":
    main()
