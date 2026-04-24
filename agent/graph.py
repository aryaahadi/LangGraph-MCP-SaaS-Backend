import asyncio
from typing import TypedDict, List
import os
from dotenv import load_dotenv

from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp.client.session import ClientSession
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import AIMessage
from langgraph.graph import StateGraph, END

load_dotenv()


class AgentState(TypedDict):
    messages: List


async def setup_agent():

    # MCP server parameters
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server.py"]
    )

    # Start MCP server via stdio
    async with stdio_client(server_params) as (read_stream, write_stream):

        # Create MCP session with read/write streams
        session = ClientSession(read_stream, write_stream)
        await session.initialize()

        # Fetch MCP tools
        tools = await session.list_tools()

        # Initialize LLM
        llm = ChatAnthropic(
            model="claude-3-5-sonnet-20241022",
            temperature=0,
            api_key=os.getenv("API_KEY"),
            client_options={
                "base_url": os.getenv("API_URL"),
            }
        ).bind_tools(tools)

        return llm, session


# Run async initialization
llm, session = asyncio.run(setup_agent())


# ---------- LangGraph Nodes ----------
def agent_node(state: AgentState):
    # Invoke LLM with the current conversation state
    response = llm.invoke(state["messages"])
    return {"messages": state["messages"] + [response]}


def tool_node(state: AgentState):
    # Extract the last tool call request from the LLM
    last = state["messages"][-1]
    tool_call = last.tool_calls[0]

    # Execute the MCP tool (sync wrapper for async call)
    result = asyncio.run(session.call_tool(
        tool_call["name"],
        tool_call["args"]
    ))

    # Return tool result as an AIMessage
    return {
        "messages": state["messages"] + [AIMessage(content=str(result))]
    }


def route(state: AgentState):
    # Decide whether to route to tool or end the graph
    last = state["messages"][-1]
    if hasattr(last, "tool_calls") and last.tool_calls:
        return "tool"
    return END


# ---------- Build LangGraph ----------
builder = StateGraph(AgentState)

builder.add_node("agent", agent_node)
builder.add_node("tool", tool_node)

builder.set_entry_point("agent")

builder.add_conditional_edges(
    "agent",
    route,
    {"tool": "tool", END: END}
)

builder.add_edge("tool", "agent")

graph = builder.compile()
