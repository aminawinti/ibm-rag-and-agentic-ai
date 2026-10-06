# Food Recommendation System

An AI-powered food recommendation system that demonstrates 3 approaches to similarity search and conversational AI. This project uses ChromaDB, Sentence Transformers, and IBM watsonx.ai (Granite) to turn a rich food dataset into an intelligent search and recommendation tool.

## Project Overview

Using a food dataset with detailed nutritional information, ingredients, cooking methods, and taste profiles, we build an interactive CLI search interface, implement advanced metadata filtering, and develop a RAG (Retrieval-Augmented Generation) chatbot that gives natural-language food recommendations.

The project shows how vector databases power real-world recommendation engines, search platforms, and conversational AI systems.

## Features

- Interactive CLI for real-time food search with similarity scores
- Advanced search combining vector similarity with cuisine and calorie filters
- RAG chatbot that retrieves relevant foods and generates answers with IBM Granite
- AI-powered comparison of two different food queries
- Side-by-side benchmark of all 3 approaches

## Project Structure

```
03-food-recommendation-system/
├── data/
│   └── FoodDataSet.json       # Food dataset
├── requirements.txt           # Dependencies
├── shared_functions.py        # Data loading, ChromaDB setup, search helpers
├── interactive_search.py      # Interactive CLI search chatbot
├── advanced_search.py         # Filtered search (cuisine, calories, combined)
├── enhanced_rag_chatbot.py    # RAG chatbot powered by IBM Granite
└── system_comparison.py       # Compares all 3 approaches
```

## Getting Started

### Installation

```bash
pip install -r requirements.txt
```

### RAG Workflow

In the enhanced chatbot, the RAG workflow looks like this:

- We load the food dataset and build a rich text description for each item
- We generate embeddings and store them in ChromaDB (cosine similarity)
- When asking a question, we retrieve the top matching foods
- We pass those foods as context to IBM Granite
- The LLM generates a personalized recommendation, with a rule-based fallback if it fails

## What I Have Learnt

- **Interactive CLI development:** building responsive command-line apps with error handling and interactive loops
- **Advanced search filtering:** combining similarity search with metadata constraints
- **RAG systems:** pairing vector search with contextual LLM responses
- **System architecture comparison:** knowing when to use simple search, advanced filtering, or conversational AI
- **Real-world applications:** recommendation engines, search platforms, and chatbots

## Technical Skills

- **ChromaDB operations:** creating collections, populating data, running similarity searches, and applying metadata filters
- **Similarity search:** using cosine similarity to find documents that closely match a query
- **Conversational AI techniques:** basic context tracking, intent recognition, and response generation
