"""
LANGGRAPH STATE — REVISED EXPLANATION

In LangGraph, "State" is a core concept that acts as a shared memory
flowing through the entire workflow.

👉 It stores ALL data needed across steps
👉 It evolves as the workflow progresses
👉 It enables intelligent, state-aware execution


==============================================================
1. ROLE OF STATE IN WORKFLOWS
==============================================================

State holds the data required to drive execution.

Example (Hiring Workflow):
    - job_description (JD)
    - approval_status
    - applicants_count
    - candidate_scores

• Stateful Execution:
    - LangGraph automatically manages state
    - No manual passing between steps

• Dynamic Evolution:
    - Each node updates state
    - Future decisions depend on updated values

👉 Think:
    "State = single source of truth"


==============================================================
2. NODE ↔ STATE INTERACTION
==============================================================

Every node interacts directly with the shared state.

• Input:
    Node receives current state

• Processing:
    Node performs task (LLM/tool/logic)

• Output:
    Node returns updated state

• Flow:
    Updated state → passed via edges to next node

• Mutability:
    - State is mutable
    - Any node can read/write/update it

👉 Think:
    "Nodes read → modify → pass state forward"


==============================================================
3. TECHNICAL IMPLEMENTATION
==============================================================

State is defined BEFORE building the graph.

Common formats:
    - TypedDict (recommended)
    - Pydantic models

Example:
    state = {
        "jd": str,
        "approved": bool,
        "score": float
    }

👉 This ensures:
    - Structured data
    - Type safety
    - Predictable workflows


==============================================================
4. REDUCERS (STATE UPDATE CONTROL)
==============================================================

By default:
    New value → replaces old value

But sometimes:
    You need accumulation (e.g., chat history)

👉 Reducers define HOW updates happen

Types:
    - Replace (default)
    - Append (add to list)
    - Merge (combine structures)

Example:
    messages = old_messages + new_messages

👉 Think:
    "Reducers control memory behavior"


==============================================================
5. PERSISTENCE & RESILIENCE (CHECKPOINTERS)
==============================================================

LangGraph can save snapshots of state at each step.

This enables:

• Fault Tolerance:
    - Resume from last saved state
    - No need to restart workflow

• Human-in-the-Loop:
    - Pause execution anytime
    - Wait for human input (minutes → days)
    - Resume from exact same point

👉 Think:
    "State + Checkpoints = Durable workflows"


==============================================================
🔥 FINAL INTUITION
==============================================================

LangChain:
    - Stateless
    - Manual state passing (glue code)

LangGraph:
    - Stateful
    - Automatic state propagation

--------------------------------------------------------------

State:
    "Memory of the system"

Nodes:
    "Modify the memory"

Edges:
    "Move the memory forward"

--------------------------------------------------------------

👉 Result:
    Clean, reliable, production-ready AI systems


==============================================================
📌 CORE MENTAL MODEL
==============================================================

Traditional Approach:
    Data passed manually between functions

LangGraph:
    Shared state flows through entire graph

👉 You don’t pass data — the graph carries it
"""