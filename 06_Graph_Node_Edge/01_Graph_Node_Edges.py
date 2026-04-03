"""
LANGGRAPH: NODES & EDGES (REVISED EXPLANATION)

In LangGraph, the relationship between nodes and edges can be understood as a
"flowchart engine" for AI workflows.

👉 Nodes define: WHAT to do
👉 Edges define: WHEN and in WHAT ORDER to do it


==============================================================
1. GRAPH NODES → "WHAT"
==============================================================

Nodes represent individual tasks (units of work) in the workflow.

• Technical Nature:
    - Each node is just a Python function

• Role in AI Systems:
    - Call an LLM
    - Use a tool (search, DB, API)
    - Perform logic / transformation

• State Interaction:
    - Input: current state (shared dictionary)
    - Process: perform task
    - Output: updated state

👉 Think:
    "Do this specific task"


==============================================================
2. GRAPH EDGES → "WHEN"
==============================================================

Edges define how execution flows between nodes.

• They act like arrows in a flowchart

• Types of Edges:

    1. Sequential:
        A → B → C

    2. Parallel:
        A → (B, C, D at same time)

    3. Conditional:
        A → (if condition → B, else → C)

    4. Loops:
        A → B → A (repeat until condition met)

👉 Think:
    "What happens next?"


==============================================================
ANALOGY: UPSC ESSAY PRACTICE SYSTEM
==============================================================

Imagine building an AI system to help students practice essays.

-------------------------
🔹 NODES (TASKS)
-------------------------

Node A → Generate Topic
    - LLM creates essay topic

Node B → Collect Essay
    - User submits essay

Node C → Evaluate Essay
    - Check clarity, depth, language

Node D → Feedback
    - Give suggestions if score is low


-------------------------
🔹 EDGES (FLOW)
-------------------------

1. Sequential Flow:
    Generate Topic → Collect Essay → Evaluate

2. Parallel Evaluation:
    Evaluate:
        → Clarity
        → Depth
        → Language
    (all run simultaneously)

3. Conditional Flow:
    If score ≥ 10:
        → END

    If score < 10:
        → Feedback → Loop back to Collect Essay

4. Loop:
    Student keeps improving until score is good


==============================================================
🔥 FINAL INTUITION
==============================================================

LangChain:
    Flow is hidden in Python (if/while → glue code)

LangGraph:
    Flow is EXPLICIT in graph (edges)

--------------------------------------------------------------

Nodes:
    "Do work"

Edges:
    "Decide what happens next"

--------------------------------------------------------------

👉 Result:
    Clean, visual, debuggable workflows
    No hidden logic
    Minimal / zero glue code


==============================================================
📌 CORE MENTAL MODEL
==============================================================

Traditional Code:
    Logic = scattered across functions + control flow

LangGraph:
    Logic = nodes
    Flow  = edges

👉 You DESIGN the system instead of stitching it
"""