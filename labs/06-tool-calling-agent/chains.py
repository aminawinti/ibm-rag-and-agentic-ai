import json

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

from tools import tool_mapping, tools

# initialize chat model
llm = init_chat_model("gpt-4o-mini", model_provider="openai")

# bind tools with the model, so it can answer with a tool call instead of text
llm_with_tools = llm.bind_tools(tools)


def execute_tool(tool_call: dict) -> ToolMessage:
    """Run one tool call requested by the LLM and wrap the result in a ToolMessage."""
    try:
        result = tool_mapping[tool_call["name"]].invoke(tool_call["args"])
        # ToolMessage content must be text
        # dicts/lists are serialized as json-formatted string
        content = json.dumps(result) if isinstance(result, (dict, list)) else str(result)
    except Exception as e:
        # LLM can read the error and retry or explain the problem to the user
        content = f"Error: {e}"

    # tool_call_id links this result to the related request
    return ToolMessage(content=content, tool_call_id=tool_call["id"])


# Automated, fixed-sequence chain
# Each RunnablePassthrough.assign keeps everything already in the state dict
# and adds one new key, so later steps can still see earlier results
fixed_chain = (
    RunnablePassthrough.assign(messages=lambda x: [HumanMessage(content=x["query"])])
    # round 1: the LLM asks for a tool (usually extract_video_id)
    | RunnablePassthrough.assign(ai_response=lambda x: llm_with_tools.invoke(x["messages"]))
    | RunnablePassthrough.assign(
        tool_messages=lambda x: [execute_tool(tc) for tc in x["ai_response"].tool_calls]
    )
    | RunnablePassthrough.assign(
        messages=lambda x: x["messages"] + [x["ai_response"]] + x["tool_messages"]
    )
    # round 2: the LLM asks for another tool (usually fetch_transcript)
    | RunnablePassthrough.assign(ai_response2=lambda x: llm_with_tools.invoke(x["messages"]))
    | RunnablePassthrough.assign(
        tool_messages2=lambda x: [execute_tool(tc) for tc in x["ai_response2"].tool_calls]
    )
    | RunnablePassthrough.assign(
        messages=lambda x: x["messages"] + [x["ai_response2"]] + x["tool_messages2"]
    )
    # final call: the answer. Anything needing a 3rd tool round, or only
    # 1 round, breaks here because the shape is fixed.
    | RunnablePassthrough.assign(summary=lambda x: llm_with_tools.invoke(x["messages"]).content)
    # the state dict has many keys by now, the user only wants the text
    | RunnableLambda(lambda x: x["summary"])
)

# Safety net (my addition, not in the lab): a confused model could keep
# requesting tools forever, which would loop and burn tokens
MAX_STEPS = 10

def should_continue(messages: list) -> bool:
    """Stopping condition: keep going only while the last message asks for tools."""
    # getattr because HumanMessage / ToolMessage have no `tool_calls` attribute
    return bool(getattr(messages[-1], "tool_calls", None))


def process_tool_calls(messages: list) -> list:
    """One round: run the tools the LLM asked for, then let the LLM react."""
    last_message = messages[-1]  # the AIMessage holding the tool calls

    # One AIMessage can request several tools at once 
    # every call needs its own ToolMessage
    tool_messages = [execute_tool(tc) for tc in last_message.tool_calls]

    updated = messages + tool_messages
    next_ai_response = llm_with_tools.invoke(updated)  # more tools, or the final answer
    return updated + [next_ai_response]


def _recursive_chain(messages: list, step: int = 0) -> list:
    """Recurse until the LLM answers without asking for a tool."""
    if not should_continue(messages):
        return messages  # base case: last message is the final answer
    if step >= MAX_STEPS:
        raise RuntimeError(f"Stopped after {MAX_STEPS} tool rounds without a final answer")
    return _recursive_chain(process_tool_calls(messages), step + 1)


# RunnableLambda makes the function a chain component, so it can sit after `|`
recursive_chain = RunnableLambda(_recursive_chain)

universal_chain = (
    RunnableLambda(lambda x: [HumanMessage(content=x["query"])])
    # first LLM call happens outside the recursion: it only starts the loop
    | RunnableLambda(lambda messages: messages + [llm_with_tools.invoke(messages)])
    | recursive_chain
)
