# Course 6 - Fundamentals of Building AI Agents

## Background note

Courses 2-5 were fixed pipelines: I decided the steps (chunk, embed, retrieve, generate) and the LLM only filled in the last one. This course flips that. The LLM can decide which tool to call and when, so the code around it becomes a loop instead of a straight line. It also starts with the question of _when_ an agent is worth using at all.

## What this course covered

- **Foundations of tool calling and chaining:** From simple LLM features to workflows to agents: the architecture, when to use an agent, and its risks
- **Tool calling:** how an LLM uses external data and functionality, and why a framework should handle it instead of the client
- **LCEL and manual tool calling:** LCEL, binding tools to an LLM, structured outputs for tool calls, and parsing and validating LLM output
- **Built-in LangChain agents:** the Pandas DataFrame agent (NL to analysis and charts) and the SQL agent (NL to database queries)

## Key concepts

Use the simplest option that does the job:

| Level              | What it is                                 | Use when                                          |
| ------------------ | ------------------------------------------ | ------------------------------------------------- |
| Simple LLM feature | A single model call                        | Basic tasks                                       |
| Workflow           | Predefined steps, like my RAG pipelines    | The task is predictable and needs to be efficient |
| Agent              | The LLM decides steps and tools on its own | Complex reasoning or adaptability is needed       |

**Is an agent the right fit?** Agents are a poor fit for simple, repeatable or high-risk tasks where errors are costly or predictable, because a plain tool does those better.

**Tool calling.** Tools connect an LLM to real-time external data and functionality. Handling tools in a dedicated library or framework, improves accuracy and reduces hallucinations.

**The tool calling steps.**

1. **Define the tool** with the `@tool` decorator, so inputs are controlled and validated
2. **Bind the tools** to the LLM (`bind_tools`) so it can pick the right one from the prompt
3. **Map names to functions** with a dictionary (e.g. `"add"` -> the add function), because the LLM only returns the tool _name_ and arguments as key-value pairs
4. **Run it** with `.invoke(input_)`, passing a dictionary whose keys match the tool's parameter names
5. **Send the result back** to the LLM so it can continue

**NOTE:** LCEL is how these steps are composed into chains with the `|` operator. This is the same idea as the retrieval chains from Courses 2-4, but here part of the chain is the LLM choosing a tool.

**Built-in agents.**

- **Zero-Shot ReAct agent:** uses zero-shot reasoning to solve tasks it hasn't seen before. Works best for simple or well-structured problems
- **Pandas DataFrame agent:** takes natural language questions and generates Python code that runs directly on the DataFrame
- **SQL agent:** translates a natural language query into SQL, runs it, and returns the results

## What I actually built

Built a YouTube tool calling agent with LangChain and OpenAI's `gpt-4o-mini`. It has five tools (video ID extraction, transcripts, search, metadata, thumbnails) and 2 ways to run the tool loop:

1. a **fixed chain** with `RunnablePassthrough.assign`, hard-coded to two tool rounds
2. a **recursive chain** that keeps going until the LLM answers without a tool call, so it handles any number of steps, including several tool calls in one turn

See the code at `labs/06-tool-calling-agent/`.

## Notes & things I'd do differently

- I'd add logging of every tool call in `execute_tool`
- The fixed chain worked for "summarize this video" and broke for anything with a different number of steps. That makes the workflow-vs-agent decision concrete: if I always know the steps, a workflow is simpler and cheaper
