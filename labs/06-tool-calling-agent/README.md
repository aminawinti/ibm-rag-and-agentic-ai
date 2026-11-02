# Build a Tool Calling Agent

A YouTube agent built with LangChain tool calling: given a natural-language request, the LLM decides which tools to call (video ID extraction, transcripts, search, metadata, thumbnails), in what order, and how many times, then writes the final answer. This project uses LangChain and OpenAI's `gpt-4o-mini`.

## Project Overview

The lab goes from an automated size-fixed tool loop (two-step chain) to an agent that decides its own number of steps (recursive chain).

## Features

- Five YouTube tools: `extract_video_id`, `fetch_transcript`, `search_youtube`, `get_full_metadata`, `get_thumbnails`
- **Recursive chain** that keeps calling tools until the LLM answers in plain text
- Fixed two-step chain, kept to show why a fixed pipeline doesn't scale
- CLI to run automated or recursive flow

## Project Structure

```
06-tool-calling-agent/
├── requirements.txt    # Dependencies
├── tools.py            # The 5 @tool functions, `tools` list, `tool_mapping`
├── chains.py           # execute_tool, fixed chain, recursive chain
└── main.py             # CLI entry point
```

## Getting Started

### Installation

```bash
pip install -r requirements.txt
```

### Running

```bash
python main.py "Show top 3 US trending videos with metadata and thumbnails"
python main.py --mode fixed  "Summarize https://www.youtube.com/watch?v=T-D1OfcDW1M"
```

`--mode` is `recursive` by default.

## Recursive Chain Flow

The main idea: the LLM signals "I need a tool" by putting `tool_calls` on its reply.
The loop is: run the requested tools → append the results → ask the LLM again → stop when the reply has no `tool_calls`

`universal_chain` = query -> `HumanMessage` -> first LLM call -> `recursive_chain`. The first LLM call sits outside the recursion because it only _starts_ the loop.

Things I added:

- Tool errors are returned as text instead of raised, so the LLM can read them and react.
- `MAX_STEPS = 10` guard: Without it a model that keeps requesting tools would recurse forever.

## Automated Tool Calling (Fixed Chain)

The same loop wired as a LangChain pipeline with `RunnablePassthrough.assign` and the `|` operator.

Each `assign` adds one key to a state dict (`messages`, `ai_response`, `tool_messages`, ...) while keeping the previous ones, and a final `RunnableLambda` returns only the summary text.

The shape is hard-coded to exactly **two** tool rounds. A request that needs one round or four breaks it, which is the reason for the recursive version above.

## What I Have Learnt

- **Tools:** `@tool` turns a function into: name, description (docstring) and argument schema
- **Binding:** `bind_tools` lets the model answer with a specific tool call
- **Message flow:** `HumanMessage` -> `AIMessage (tool_calls)` -> `ToolMessage` -> `AIMessage`, linked by `tool_call_id`
- **Recursion as agent loop:** a stopping condition plus a step function replaces a fixed number of steps
- **Composing chains:** `RunnablePassthrough.assign` for keeping state, `RunnableLambda` for plain functions
