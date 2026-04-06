"""
LangGraph Conditional Workflow (Sentiment → Routing → Response)

Flow:
START → find_sentiment → (conditional)
        → positive_response
        → negative_response
        → END
"""

# ================================
# Imports
# ================================
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field


# ================================
# Initialize LLM (Ollama)
# ================================
model = ChatOllama(
    model="llama3.1:8b",
    temperature=0
)


# ================================
# Structured Output Schema
# ================================
class SentimentSchema(BaseModel):
    sentiment: Literal["positive", "negative"] = Field(
        description="Sentiment of the review"
    )


# Wrap model for structured output
structured_model = model.with_structured_output(SentimentSchema)


# ================================
# Define State
# ================================
class ReviewState(TypedDict):
    review: str
    sentiment: Literal["positive", "negative"]
    response: str


# ================================
# Node 1: Find Sentiment
# ================================
def find_sentiment(state: ReviewState) -> dict:
    prompt = f"""
    Analyze the sentiment of the following review:
    {state['review']}
    """

    result = structured_model.invoke(prompt)

    return {"sentiment": result.sentiment}


# ================================
# Node 2A: Positive Response
# ================================
def positive_response(state: ReviewState) -> dict:
    return {
        "response": f"😊 Thanks for your positive feedback! Glad you liked it."
    }


# ================================
# Node 2B: Negative Response
# ================================
def negative_response(state: ReviewState) -> dict:
    return {
        "response": f"😔 Sorry to hear that. We'll work on improving."
    }


# ================================
# Routing Function (IMPORTANT)
# ================================
def route_sentiment(state: ReviewState) -> str:
    if state["sentiment"] == "positive":
        return "positive_response"
    else:
        return "negative_response"


# ================================
# Build Graph
# ================================
builder = StateGraph(ReviewState)

# Nodes
builder.add_node("find_sentiment", find_sentiment)
builder.add_node("positive_response", positive_response)
builder.add_node("negative_response", negative_response)

# Start → sentiment
builder.add_edge(START, "find_sentiment")

# Conditional branching
builder.add_conditional_edges(
    "find_sentiment",
    route_sentiment,
    {
        "positive_response": "positive_response",
        "negative_response": "negative_response",
    }
)

# End edges
builder.add_edge("positive_response", END)
builder.add_edge("negative_response", END)

# Compile
graph = builder.compile()


# ================================
# Execute
# ================================
initial_state = {
    "review": "The product was really bad",
    "sentiment": "positive",   # placeholder
    "response": ""
}

result = graph.invoke(initial_state)

print("\n=== FINAL OUTPUT ===\n")
print(result)


# === FINAL OUTPUT ===

# {
# 'review': 'The product was really bad', 
# 'sentiment': 'negative', 
# 'response': "😔 Sorry to hear that. We'll work on improving."
# }


"""
LangGraph Conditional Workflow (Sentiment → Routing → Response)

Purpose
-------
Route execution based on LLM output.

Input review → detect sentiment → choose correct response path


------------------------------------------------------------
1️⃣ State (Shared Data)
------------------------------------------------------------

class ReviewState(TypedDict):
    review: str
    sentiment: "positive" | "negative"
    response: str

• review → input text
• sentiment → decided by LLM
• response → generated based on sentiment

State flows across all nodes


------------------------------------------------------------
2️⃣ Structured Output (IMPORTANT)
------------------------------------------------------------

class SentimentSchema(BaseModel):
    sentiment: Literal["positive", "negative"]

structured_model = model.with_structured_output(...)

Why this matters:
✔ Forces LLM to return ONLY valid values
✔ Prevents messy outputs like:
   "It seems somewhat positive..."

Instead:
✔ Always → "positive" or "negative"


------------------------------------------------------------
3️⃣ Node 1 → find_sentiment
------------------------------------------------------------

def find_sentiment(state):

• Reads → review
• Sends to LLM
• Returns → {"sentiment": "positive" / "negative"}

This is the "decision-making" step


------------------------------------------------------------
4️⃣ Routing Function (CORE IDEA)
------------------------------------------------------------

def route_sentiment(state):
    if sentiment == "positive":
        return "positive_response"
    else:
        return "negative_response"

This function:
✔ does NOT generate data
✔ ONLY decides "where to go next"

Think:
Router = traffic signal of the graph


------------------------------------------------------------
5️⃣ Conditional Edges (IMPORTANT)
------------------------------------------------------------

builder.add_conditional_edges(
    "find_sentiment",
    route_sentiment,
    {
        "positive_response": "positive_response",
        "negative_response": "negative_response",
    }
)

What happens:

After find_sentiment:
→ route_sentiment decides next node
→ graph jumps dynamically

This is NOT fixed flow anymore


------------------------------------------------------------
6️⃣ Response Nodes
------------------------------------------------------------

positive_response:
✔ returns friendly message

negative_response:
✔ returns apology message

• Both write → "response"


------------------------------------------------------------
7️⃣ Execution Flow
------------------------------------------------------------

Input:
"The product was really bad"

Step 1:
find_sentiment → "negative"

Step 2:
route_sentiment → chooses "negative_response"

Step 3:
negative_response → generates reply

Final Output:
{
    review,
    sentiment="negative",
    response="Sorry..."
}


------------------------------------------------------------
8️⃣ Key Concept → Conditional Graphs
------------------------------------------------------------

Unlike normal flow:

START → A → B → END

Here:

START → A → (decision)
              ↙      ↘
        positive   negative

✔ Path depends on runtime data
✔ Graph becomes dynamic


------------------------------------------------------------
9️⃣ Why This Matters
------------------------------------------------------------

This pattern is used in:

• AI agents (tool selection)
• Chatbots (intent routing)
• Customer support systems
• Decision engines

General idea:
Analyze → Decide → Act


------------------------------------------------------------
Key Takeaway
------------------------------------------------------------

LangGraph enables dynamic workflows:

• LLM makes decision (sentiment)
• Router picks next step
• Different paths execute

This is the foundation of intelligent AI systems.
"""