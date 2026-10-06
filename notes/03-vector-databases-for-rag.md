# Course 3 - Vector Databases for RAG: An Introduction

## Background note

Course 2 treated the vector store as a black box inside the RAG pipeline. This course opens that box: what a vector database is, how it differs from a traditional one, and how to work with it directly using ChromaDB.

## What this course covered

- **Vector databases vs. traditional databases:** what they store, how they search, and where each fits
- **ChromaDB** as the hands-on tool: architecture, collections, embeddings, and metadata filtering
- **Similarity search**, done both manually and with ChromaDB
- **Recommendation systems** built on similarity search
- **The vector database's role inside RAG**, and which pipeline steps happen outside it

## Key concepts

**Vector databases.** A vector is an array of numbers describing the features of an item (text, image, audio, etc.). Vector databases store and index these vectors so that "similar" items can be found quickly, which powers recommendations, document search, image retrieval, and chatbots.

**ChromaDB.** A vector database that supports vector search, metadata filtering, full-text search, and multi-modal retrieval. It uses ANN search to find the closest matches efficiently.

**Vector databases in RAG.** The database embeds and stores documents, embeds the user's prompt, retrieves the best matches, and supplies them for prompt augmentation. Chunking, advanced retrieval logic, prompt augmentation, and the LLM call usually happen **outside** the database, and frameworks like LangChain and LlamaIndex can manage the full pipeline around it.

## What I actually built

Built a Food Recommendation System with ChromaDB, implementing 3 approaches to the same problem. Also, wrote a comparison script for these approaches:

1. interactive CLI similarity search
2. advanced search with cuisine and calorie metadata filters
3. RAG chatbot using model to generate natural-language recommendations.

See snippets from this app at `labs/03-food-recommendation-system/`

## Notes & things I'd do differently

- Chunking lives outside the database, so the chunk size question from Course 2 is still open. I'll dig into it in Course 4
- Metadata filtering made search far more precise than similarity alone, but it needs clean, consistent metadata (e.g. exact cuisine names)
