# AI-Powered YouTube Summarizer

A question-answering tool that summarizes YouTube videos and answers specific questions about them, based on the video's transcript. This project uses LangChain, IBM watsonx.ai and Gradio.

## Project Overview

This tool fetches a video's transcript, summarizes it with an LLM, and lets you ask follow-up questions. It works with the main components of a RAG application: a transcript loader, a text splitter, an embedding model, a vector database, a retriever and a user-friendly interface.

## Features

- Fetch the English transcript of a video (manual captions are preferred over auto-generated ones)
- Summarize the video in a single paragraph
- Answer questions about the video using retrieval over the transcript
- Gradio web interface

## Project Structure

```
04-ai-powered-yt-summarizer/
├── requirements.txt           # Dependencies
├── config.py                  # Central settings
├── app.py                     # Gradio interface
└── modules/
    ├── transcript.py          # Fetch, format and chunk transcripts
    ├── llm_interface.py       # watsonx LLM and embedding model
    ├── prompts.py             # Summary and Q&A prompt templates
    └── query_engine.py        # Summarization, FAISS index, Q&A
```

## Getting Started

### Installation & Running

```bash
pip install -r requirements.txt

python app.py
```

Open http://localhost:7860, paste a YouTube URL. The video needs English captions ONLY. other languages support may be added in the future.

### RAG Workflow

**Summary:** transcript -> LLM -> one-paragraph summary

**Q&A:**

1. Transcript is split into small chunks (200 characters, 20 overlap)
2. Each chunk is embedded and stored in a FAISS index
3. The question retrieves the 7 most similar chunks
4. The LLM answers the question using only those chunks as context

## What I Have Learnt

- **Transcript processing:** fetching a transcript and formatting it with timestamps so the LLM can use them as context
- **Summarization:** prompting an LLM for concise summaries
- **Retrieval-based Q&A:** chunking, embeddings and similarity search to answer questions from relevant parts of a long text
- **User interface:** wrapping the pipeline in a Gradio app

## Technical Skills

- **LangChain:** prompt templates, LLM chains, text splitters, FAISS vector store
- **watsonx.ai integration:** Granite LLM and embedding model through `langchain-ibm`
- **Gradio:** building an interactive web UI

## Next Steps

- Add sentiment analysis on the transcript
- Support for summarizing videos in other languages
- Recommend similar videos
