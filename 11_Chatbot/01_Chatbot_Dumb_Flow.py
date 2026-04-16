from langgraph.graph import StateGraph, START, END
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph.message import add_messages
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict, Annotated

# CHAT STATE
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# LLM
# defined globally for node access
llm = ChatOllama(model="mistral:7b", temperature=0)


# NODE 1 : Chat Node
def chat_node(state: ChatState):
    # get conversation history
    messages = state["messages"]

    # call LLM
    response = llm.invoke(messages)

    # append response to state
    return {"messages": [response]}


# GRAPH
# initialize graph
graph = StateGraph(ChatState)

# add nodes
graph.add_node('chat_node', chat_node)

# define flow (edges)
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

# compile graph
memory = MemorySaver()
app = graph.compile(checkpointer=memory)


if __name__ == "__main__":
    thread_id = input("Enter session id (e.g. user_1): ").strip() or "default"

    print("Type 'exit', 'quit', or 'bye' to stop.\n")

    while True:
        user_input = input("You: ")

        if user_input.strip().casefold() in ["exit", "quit", "bye"]:
            print("Exiting chat...")
            break

        result = app.invoke(
            {
                "messages": [HumanMessage(content=user_input)]
            },
            config={"configurable": {"thread_id": thread_id}}
        )

        print("AI:", result["messages"][-1].content)