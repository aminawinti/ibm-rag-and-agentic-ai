# Advanced Retrievers in LlamaIndex

Six retrieval strategies in LlamaIndex, run and compared side by side. This project uses IBM watsonx.ai for LLM calls and a HuggingFace embedding model for vector search.

## Project Overview

Basic vector search is a good default, but it breaks down on: exact keywords, long documents, ambiguous queries and large collections. Each script runs one group of retrievers on small set of documents, so every result can be read and judged directly. Then we combine them showcasing their power in: hybrid_retriever & rag_pipeline.

## Retrievers Usage

`VectorIndexRetriever`: general semantic search  
`BM25Retriever`: exact terms matter  
`DocumentSummaryIndex`: large, diverse collections  
`AutoMergingRetriever`: long documents  
`RecursiveRetriever`: citations, summaries pointing at full text  
`QueryFusionRetriever`: ambiguous queries, hybrid search

## Project Structure

```
04-advanced-retrievers-llamaindex/
├── requirements.txt           # Dependencies
├── config.py                  # Central settings
├── shared.py                  # Model setup, index builders, etc
├── basic_retrievers.py        # vector, BM25, document summary
├── context_retrievers.py      # auto merging, recursive
├── query_fusion.py            # With 3 fusion modes
├── hybrid_retriever.py        # Demo 1: vector + BM25 hybrid
└── rag_pipeline.py            # Demo 2: RAG pipeline
```

Each script is standalone and builds only the indexes it needs. The document summary index costs one LLM call per document, so only `basic_retrievers.py` and `context_retrievers.py` pay for it.

## Getting Started

### Installation & Running

```bash
pip install -r requirements.txt

#
python basic_retrievers.py
python context_retrievers.py
python query_fusion.py
python hybrid_retriever.py
python rag_pipeline.py
```

## Recommended Retrievers by Use Case

1. General Q&A Applications:
   - Primary: Vector Index
   - Enhancement: Combine with BM25 Retriever using Query Fusion
2. Technical Documentation:
   - Primary: BM25
   - Enhancement: Vector Index
3. Long Documents:
   - Primary: Auto Merging
4. Research Papers:
   - Primary: Recursive
5. Large Document Collections:
   - Primary: Document Summary Index
   - Enhancement: Vector Index

## What I Have Learnt

- **Vector vs keyword search:** they fail in opposite ways (BM25 misses synonyms, embeddings miss exact terms), which is why hybrid search is the common production pattern
- **Compact representations:** Document Summary and Recursive retrievers both search small summaries but return full content, via filtering and via pointers respectively
- **Hierarchical chunking:** Auto Merging keeps precise matching on small chunks while returning larger parents for context, at the price of extra storage
- **Fusion strategies:** RRF uses ranks only, relative score uses min-max scaled scores, distribution-based scaling uses mean ± 3σ bounds to resist outliers
- **Pipeline design:** routing, graceful fallback when the LLM fails, and a simple success-rate evaluation

## Technical Skills

- **LlamaIndex retrieval:** building indexes, retrievers, node parsers and storage contexts
- **Retrieval evaluation by inspection:** reading scores and rankings across strategies on the same queries
