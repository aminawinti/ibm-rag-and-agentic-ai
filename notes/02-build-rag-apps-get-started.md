# Course 2 - Build RAG Applications: Get Started

## Background note

Course 1 was about calling an LLM directly. This course moved into actual RAG: grounding answers in your own data instead of relying only on what the model already knows.

## What this course covered

- Why **RAG** is useful, and the full RAG pipeline: sources → chunking → embedding → vector store → retriever → prompt augmentation → LLM → response
- **LlamaIndex** as a second framework for building RAG apps (alongside LangChain from Course 1)
- **Gradio** for building a quick UI on top of a RAG pipeline, as an alternative to Flask

## Key concepts

The RAG pipeline, step by step:

**Why RAG?** You could just paste everything into the prompt, but that's limited by context size, can bury relevant facts in irrelevant text, and costs more. RAG fixes this by only retrieving the relevant pieces of text instead of sending everything.

**The RAG pipeline:**

1. Split documents into chunks
2. Turn chunks into vectors (embeddings) and store them in a vector database (ChromaDB)
3. Turn the user's question into a vector too, using the same embedding model
4. Find the most similar chunks (similarity search)
5. Add those chunks to the prompt and send it to the LLM

**LlamaIndex vs. LangChain.** Both help you build LLM apps. LlamaIndex is simpler and faster to get started with — it handles embedding + storage in one step (`VectorStoreIndex`), and can even handle retrieval + answering in one step (a "query engine"). LangChain is more flexible and has more integrations, but needs more manual wiring.

**Gradio.** A Python package that builds a simple UI for you — no HTML/CSS/JS needed. You wrap a function with `Interface(fn, inputs, outputs)`, and `launch()` starts a local (or public, with `share=True`) web app.

## What I actually built

Built an AI Icebreaker Bot with LlamaIndex: it researches a person’s LinkedIn profile and generates personalized conversation starters based on their career highlights, interests, and fun facts. Used Gradio for the UI, allowing users to enter a name and get tailored icebreakers for networking and introductions.

See snippets from this app at `labs/02-linkedin-icebreaker-bot/`

## Notes & things I'd do differently

- Gradio is faster for a demo, but Flask gives more control — which fits my React/TS background better if I want a custom UI
- Chunk size matters more than I expected — want to dig into this more in Course 3/4
- Want to try building the same thing manually in LangChain, to actually feel the difference vs. LlamaIndex's query engine
