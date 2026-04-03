"""
LANGGRAPH REDUCERS — REVISED EXPLANATION

In LangGraph, "Reducers" define HOW updates from nodes are applied
to the shared State.

👉 They control how new data interacts with existing data
👉 They are essential for managing state correctly in complex workflows


==============================================================
1. WHAT REDUCERS DO (UPDATE LOGIC)
==============================================================

When a node updates State:

Default behavior:
    New value → REPLACES old value

Reducers allow you to change this behavior:

    - Replace     → overwrite old value
    - Append      → add to existing value (e.g., list)
    - Merge       → combine structures (e.g., dicts)

👉 Think:
    "Reducer = rule for updating memory"


==============================================================
2. WHY REDUCERS ARE IMPORTANT
==============================================================

Reducers are critical when simple replacement is NOT enough.

--------------------------------------------------------------

A. Prevent Data Loss

Problem:
    Updating state removes previous data

Example:
    Chatbot messages:
        Without reducer → old messages lost
        With reducer → messages appended

👉 Ensures full history is preserved


--------------------------------------------------------------

B. Handle Parallel Updates

Problem:
    Multiple nodes update state at same time

Example:
    Parallel tasks:
        → Task A updates "results"
        → Task B updates "results"

Reducer:
    Defines how both updates combine

👉 Prevents conflicts and lost updates


--------------------------------------------------------------

C. Fine-Grained Control per Key

Each state key can have its own rule:

Example:
    "status"         → replace
    "messages"       → append
    "scores"         → merge

👉 Flexible and customizable state behavior


==============================================================
3. PRACTICAL EXAMPLE (UPSC ESSAY SYSTEM)
==============================================================

Scenario:
    Student writes multiple essay drafts

--------------------------------------------------------------

Without Reducer:
    essay = "Draft 1"
    essay = "Draft 2"

👉 Result:
    Draft 1 is LOST


--------------------------------------------------------------

With Reducer (Append):

    essays = ["Draft 1"]
    essays = ["Draft 1", "Draft 2"]

👉 Result:
    Full history preserved
    Student can track improvement over time


==============================================================
4. TECHNICAL IMPLEMENTATION
==============================================================

State is defined using structured schema:

    - TypedDict
    - Pydantic models

Reducers are assigned per key.

Conceptually:

    state = {
        "messages": append_reducer,
        "status": replace_reducer
    }

In practice:
    Python uses annotations (e.g., Annotated)

👉 This tells LangGraph:
    HOW to handle updates for each field


==============================================================
🔥 FINAL INTUITION
==============================================================

State:
    "What data exists"

Reducers:
    "How data changes over time"

--------------------------------------------------------------

Without reducers:
    ❌ Data overwritten
    ❌ History lost
    ❌ Conflicts in parallel flows

With reducers:
    ✅ Controlled updates
    ✅ History preserved
    ✅ Safe parallel execution


==============================================================
📌 CORE MENTAL MODEL
==============================================================

Traditional Code:
    You manually control data updates

LangGraph:
    You DEFINE update rules (reducers)

👉 System handles consistency automatically
"""