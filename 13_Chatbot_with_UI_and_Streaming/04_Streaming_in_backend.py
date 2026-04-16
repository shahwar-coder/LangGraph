from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, BaseMessage
from langgraph.graph.message import add_messages
from langchain_ollama import ChatOllama
from typing import TypedDict, Annotated


# ----------------------------
# STATE
# ----------------------------
class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


# ----------------------------
# LLM (streaming enabled)
# ----------------------------
llm = ChatOllama(model="mistral:7b", temperature=0)


# ----------------------------
# NODE
# ----------------------------
def chat_node(state: State):
    messages = state.get("messages", [])

    # stream response
    response_chunks = []
    for chunk in llm.stream(messages):
        print(chunk.content, end="", flush=True)   # 👈 streaming output
        response_chunks.append(chunk)

    print()  # newline after completion

    # combine chunks into final message
    final_response = response_chunks[-1]

    return {"messages": [final_response]}


# ----------------------------
# GRAPH
# ----------------------------
graph = StateGraph(State)
graph.add_node("chat_node", chat_node)

graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

app = graph.compile()


# ----------------------------
# RUN
# ----------------------------
if __name__ == "__main__":
    user_input = input("You: ")

    result = app.invoke({
        "messages": [HumanMessage(content=user_input)]
    })

    print("\nFinal stored response:")
    print(result["messages"][-1].content)



"""
Upgrade: Streaming in LangGraph Backend

What Changed
------------
Instead of waiting for the full LLM response,
we now receive and display output token-by-token (chunk-by-chunk).


------------------------------------------------------------
1️⃣ Streaming vs Normal Invocation
------------------------------------------------------------

Normal:
response = llm.invoke(messages)
→ waits for full response → then prints

Streaming:
for chunk in llm.stream(messages):
→ receives partial output continuously

Benefit:
✔ real-time output
✔ better UX (feels faster)


------------------------------------------------------------
2️⃣ How Streaming Works Here
------------------------------------------------------------

response_chunks = []

for chunk in llm.stream(messages):
    print(chunk.content, end="", flush=True)
    response_chunks.append(chunk)

• llm.stream() yields small pieces of response
• Each chunk contains partial text
• Printed immediately → live output


------------------------------------------------------------
3️⃣ Why `flush=True`?
------------------------------------------------------------

print(..., flush=True)

• Forces immediate display in terminal
• Without it → output may buffer (delay)


------------------------------------------------------------
4️⃣ Reconstructing Final Response
------------------------------------------------------------

final_response = response_chunks[-1]

• Last chunk contains full accumulated message
• Stored back into state

Important:
✔ streaming is for display
✔ final message is still needed for state


------------------------------------------------------------
5️⃣ Integration with LangGraph State
------------------------------------------------------------

return {"messages": [final_response]}

• Only final response is stored
• Full history maintained via add_messages

So:
✔ UI gets streaming
✔ Graph gets clean final state


------------------------------------------------------------
6️⃣ Why This Matters (Backend Systems)
------------------------------------------------------------

Streaming is used in:

• ChatGPT-like interfaces
• Live assistants
• Real-time dashboards
• Long response generation

Benefits:
✔ faster perceived response
✔ better interactivity
✔ improved user experience


------------------------------------------------------------
Key Takeaway
------------------------------------------------------------

Streaming = incremental output delivery

LangGraph still:
✔ maintains structured state
✔ stores final response

But user sees:
✔ real-time generation instead of waiting
"""