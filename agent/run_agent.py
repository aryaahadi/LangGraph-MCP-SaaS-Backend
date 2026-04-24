from langchain_core.messages import HumanMessage
from graph import graph

def run():

    query = """
A customer (ID 200) is complaining that they can't invite another user.
Check if they are over the seat limit. If yes, upgrade them to the starter plan.
Then open a support ticket explaining what happened.
"""

    state = {"messages": [HumanMessage(content=query)]}

    result = graph.invoke(state)

    for msg in result["messages"]:
        print("\n--- MESSAGE ---\n", msg)


if __name__ == "__main__":
    run()
