"""
LANGGRAPH EXECUTION MODEL — QUICK REVISION

==============================================================
🔹 CORE IDEA
==============================================================

LangGraph executes workflows as a graph:
    Nodes (tasks) + Edges (flow) + State (data)

👉 Execution is automatic, not manually controlled


==============================================================
🔹 1. LIFECYCLE
==============================================================

1. Define:
    Nodes + Edges + State

2. Compile:
    Validate graph (no errors)

3. Execute:
    graph.invoke(initial_state)


==============================================================
🔹 2. EXECUTION FLOW
==============================================================

• Node receives state → runs function
• Returns partial update
• State flows to next node via edges

👉 No manual data passing


==============================================================
🔹 3. SUPERSTEPS
==============================================================

• Execution happens in rounds (supersteps)
• Multiple nodes can run in parallel
• Updates are merged using reducers

👉 Parallel + synchronized execution


==============================================================
🔹 4. TERMINATION
==============================================================

Stops when:
    - No active nodes
    - No state updates remaining


==============================================================
🔥 FINAL INTUITION
==============================================================

LangGraph =
    "Design graph → System runs it"

--------------------------------------------------------------

Nodes:
    Do work

Edges:
    Control flow

State:
    Carries data

Supersteps:
    Execution cycles

--------------------------------------------------------------

👉 You define the system,
👉 LangGraph handles execution
"""