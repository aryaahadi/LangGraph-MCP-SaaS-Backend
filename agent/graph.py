from langgraph.graph import StateGraph, END
from typing import TypedDict, List
from dotenv import load_dotenv

from langchain_core.messages import HumanMessage, AIMessage
from langchain_anthropic import ChatAnthropic

from mcp.client import MCPClient



load_dotenv()


class AgentState(TypedDict):
    messages: List


# Connect to MCP server (via stdio)
mcp_client = MCPClient(
    mode="stdio",
    command="python",
    args=["mcp_server.py"]
)

tools = mcp_client.get_tools()

llm = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    temperature=0
).bind_tools(tools)


def agent_node(state: AgentState):
    response = llm.invoke(state["messages"])
    return {"messages": state["messages"] + [response]}


def tool_node(state: AgentState):
    last = state["messages"][-1]
    tool_call = last.tool_calls[0]

    result = mcp_client.call_tool(
        tool_call["name"],
        tool_call["args"]
    )

    return {
        "messages": state["messages"] + [
            AIMessage(content=str(result))
        ]
    }


def route(state: AgentState):
    last = state["messages"][-1]
    if hasattr(last, "tool_calls") and last.tool_calls:
        return "tool"
    return END


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
