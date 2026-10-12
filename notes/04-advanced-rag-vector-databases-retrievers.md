# Course 4 - Advanced RAG with Vector Databases and Retrievers

## Background note

Course 3 opened the vector database box; this course improves what comes out of it. Basic similarity search is only the starting point. Better retrieval (more diverse, filtered, context-aware, or hybrid) is what makes a RAG app's answers noticeably better. The second half picks the vector database itself (FAISS vs. Chroma DB) and assembles a full app.

## What this course covered

- **Advanced retrievers in LangChain:** vector store-backed, multi-query, self-query, parent document
- **Index types and retrievers in LlamaIndex:** core vs. advanced retrievers, and fusing results from several of them
- **FAISS vs. Chroma DB:** indexing algorithms (LSH, HNSW), and extending FAISS with Milvus
- **An end-to-end RAG app:** LangChain + FAISS + an advanced retriever + a Gradio UI

## Key concepts

**LangChain retrievers:** The basic one is vector store-backed: you create it from the vector store object with `.as_retriever()`, using either:

- **Similarity search**, which returns the most similar chunks.
- **MMR (Maximal Marginal Relevance)**, which balances relevance against diversity.

**Advanced LangChain retrievers:**

| Retriever       | What it does                                                                                 | Use when                                                    |
| --------------- | -------------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| Multi-query     | An LLM rewrites the query into several variants; results are merged                          | Queries are vague or phrased differently from the documents |
| Self-query      | Splits the query into a semantic string + a metadata filter                                  | Documents have rich metadata (year, category, author)       |
| Parent document | Small child chunks are embedded for precise matching, but the large parent chunk is returned | You need precise search _and_ enough context                |

**NOTE:** The parent document retriever is a direct answer to my open chunk-size question from Courses 2 and 3: small chunks embed better, big chunks give the LLM more context, and this uses both.

**LlamaIndex index types.**

- `VectorStoreIndex`: stores an embedding per chunk. Best for semantic retrieval and the default for LLM pipelines.
- `DocumentSummaryIndex`: stores document summaries and uses them to filter before fetching full content. Good for large, diverse document sets.
- `KeywordTableIndex`: maps extracted keywords to chunks. Good for hybrid or rule-based search.

**LlamaIndex retrievers.**

- **Vector Index Retriever:** semantic search, the general-purpose choice.
- **BM25 Retriever:** keyword ranking based on exact matches, not meaning (the TF-IDF family).
- **Document Summary Index Retriever:** searches summaries instead of full text, in an LLM-based or an embedding-based version.
- **Auto Merging Retriever:** chunks hierarchically into parent/child nodes and merges up to the parent to preserve context.
- **Recursive Retriever:** follows relationships between nodes, such as citations or metadata links.
- **Query Fusion Retriever:** combines results from several retrievers using **Reciprocal Rank Fusion**, **Relative Score Fusion**, or **Distribution-Based Fusion**.

**FAISS vs. Chroma DB:**

- FAISS:
  - _Feature:_ Fine control over indexing, very fast search
  - _Limitation:_ No metadata or distribution by default
- Chroma DB:
  - _Feature:_ Easy to deploy, built-in metadata support
  - _Limitation:_ Fewer indexing options

**Indexing algorithms**

- **LSH** (locality-sensitive hashing, which hashes similar vectors into the same buckets)
- **HNSW** (hierarchical navigable small world, a layered graph for fast approximate search).
- FAISS can be extended with **Milvus** for scalability and metadata, and both tools plug into LangChain or LlamaIndex.

## What I actually built

Two main labs for this course:

1. **Advanced retrievers with LlamaIndex**
2. **AI-powered YouTube summarizer**, a RAG app using FAISS, an advanced retriever, and a Gradio UI

See `labs/04-advanced-retrievers-llamaindex/` and `labs/04-ai-powered-yt-summarizer/`.

## Notes & things I'd do differently

- Self-query only works if metadata is clean, which is the same lesson as Course 3's metadata filtering
