from langgraph.graph import StateGraph, START, END
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph.message import add_messages
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import InMemorySaver
from typing import TypedDict, Annotated


# ----------------------------
# STATE
# ----------------------------
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


# ----------------------------
# LLM
# ----------------------------
llm = ChatOllama(model="mistral:7b", temperature=0)


# ----------------------------
# NODE 1: Generate Joke
# ----------------------------
def gen_joke(state: ChatState):
    messages = state.get("messages", [])

    prompt = HumanMessage(content="Tell me a short joke.")
    response = llm.invoke(messages + [prompt])

    return {"messages": [prompt, response]}


# ----------------------------
# NODE 2: Explain Joke
# ----------------------------
def gen_exp(state: ChatState):
    messages = state.get("messages", [])

    prompt = HumanMessage(content="Explain the above joke in simple terms.")
    response = llm.invoke(messages + [prompt])

    return {"messages": [prompt, response]}


# ----------------------------
# GRAPH
# ----------------------------
graph = StateGraph(ChatState)

graph.add_node("gen_joke", gen_joke)
graph.add_node("gen_exp", gen_exp)

graph.add_edge(START, "gen_joke")
graph.add_edge("gen_joke", "gen_exp")
graph.add_edge("gen_exp", END)


# ----------------------------
# CHECKPOINTER
# ----------------------------
memory = InMemorySaver()

app = graph.compile(checkpointer=memory)


# ----------------------------
# RUN
# ----------------------------
if __name__ == "__main__":
    thread_id = "joke_session_1"

    result = app.invoke(
        {"messages": []},   # initial empty state
        config={"configurable": {"thread_id": thread_id}}
    )

    print("\n--- Final Output ---\n")
    for msg in result["messages"]:
        if isinstance(msg, AIMessage):
            print("AI:", msg.content)



# --- Final Output ---

# AI:  Sure, here's a classic one for you:

# Why don't scientists trust atoms?

# Because they make up everything!
# AI:  The joke is making fun of the fact that atoms are the basic building blocks of all matter, including living organisms and everything around us. So, if atoms are so important, it might seem strange that scientists wouldn't trust them. But the punchline "Because they make up everything!" explains why they don't need to trust them because they are everywhere and can't be avoided or distrusted.