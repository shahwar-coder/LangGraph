"""
LangGraph + Ollama Blog Generator Workflow

Flow:
Title → Outline → Blog Content
"""

# ================================
# Imports
# ================================
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_ollama import ChatOllama


# ================================
# Initialize LLM (Ollama)
# ================================
model = ChatOllama(
    model="llama3.1:8b",
    temperature=0.7   # slightly creative for writing
)


# ================================
# Define State
# ================================
class BlogState(TypedDict):
    title: str
    outline: str
    content: str


# ================================
# Node 1: Generate Outline
# ================================
def create_outline(state: BlogState) -> dict:
    title = state["title"]

    prompt = f"""
    Generate a detailed blog outline for the topic:
    {title}

    Include headings and subheadings.
    """

    response = model.invoke(prompt)

    return {"outline": response.content}


# ================================
# Node 2: Generate Blog
# ================================
def create_blog(state: BlogState) -> dict:
    title = state["title"]
    outline = state["outline"]

    prompt = f"""
    Write a detailed blog on the topic: {title}

    Use the following outline:
    {outline}

    Make it well-structured and engaging.
    """

    response = model.invoke(prompt)

    return {"content": response.content}


# ================================
# Build Graph
# ================================
builder = StateGraph(BlogState)

builder.add_node("create_outline", create_outline)
builder.add_node("create_blog", create_blog)

# Flow: START → outline → blog → END
builder.add_edge(START, "create_outline")
builder.add_edge("create_outline", "create_blog")
builder.add_edge("create_blog", END)

graph = builder.compile()


# ================================
# Execute
# ================================
initial_state = {
    "title": "Rise of AI in India",
    "outline": "",
    "content": ""
}

result = graph.invoke(initial_state)

print("\n=== FINAL OUTPUT ===\n")
print(result["content"])


"""
LangGraph + Ollama Blog Generator Workflow

Purpose
-------
Automate blog creation using a structured pipeline:

Title → Outline → Full Blog Content

Instead of one big LLM call, we break it into steps
for better quality and control.


------------------------------------------------------------
1️⃣ State (Shared Data Across Steps)
------------------------------------------------------------

class BlogState(TypedDict):
    title: str
    outline: str
    content: str

• title   → input
• outline → generated in step 1
• content → generated in step 2

Think:
State = shared memory updated step-by-step


------------------------------------------------------------
2️⃣ LLM Setup
------------------------------------------------------------

model = ChatOllama(
    model="llama3.1:8b",
    temperature=0.7
)

• temperature=0.7 → more creative output
• Good for writing tasks (blogs, stories)


------------------------------------------------------------
3️⃣ Node 1 → create_outline
------------------------------------------------------------

def create_outline(state):
    uses title → generates outline

Flow:
Input → title  
LLM → generates headings/subheadings  
Output → {"outline": ...}

Key Idea:
✔ Break complex generation into smaller steps
✔ Outline improves structure of final content


------------------------------------------------------------
4️⃣ Node 2 → create_blog
------------------------------------------------------------

def create_blog(state):
    uses title + outline → generates blog

Flow:
Input → title + outline  
LLM → expands into full blog  
Output → {"content": ...}

Why this is powerful:
✔ LLM writes with guidance (outline)
✔ More coherent and structured output


------------------------------------------------------------
5️⃣ Graph Construction
------------------------------------------------------------

builder = StateGraph(BlogState)

Nodes:
create_outline → create_blog

Flow:
START → create_outline → create_blog → END

• Sequential pipeline
• Each step depends on previous output


------------------------------------------------------------
6️⃣ Execution Flow
------------------------------------------------------------

Initial Input:
{
    "title": "Rise of AI in India",
    "outline": "",
    "content": ""
}

Step 1:
create_outline → adds outline

Step 2:
create_blog → uses outline → adds content

Final Output:
{
    "title": "...",
    "outline": "...",
    "content": "FULL BLOG"
}


------------------------------------------------------------
7️⃣ Key Concept → Chained Generation
------------------------------------------------------------

Instead of:
❌ Direct: Title → Blog (low control)

We do:
✔ Title → Outline → Blog

Benefits:
• Better structure
• More relevant content
• Less hallucination


------------------------------------------------------------
8️⃣ Why This Matters (Real Systems)
------------------------------------------------------------

This pattern is used in:

• Content generation tools
• Research assistants
• Report generation systems

General Pattern:
Step 1 → Plan  
Step 2 → Execute  
Step 3 → Refine (optional)


------------------------------------------------------------
Key Takeaway
------------------------------------------------------------

LangGraph enables structured LLM workflows:

Input → Planning Node → Execution Node → Output

This makes AI outputs:
✔ more reliable
✔ more controllable
✔ production-ready
"""