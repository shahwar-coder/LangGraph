"""
LANGGRAPH EXECUTION MODEL — REVISED EXPLANATION

LangGraph follows a structured execution model inspired by systems like Google Pregel,
designed for scalable, graph-based computation.

👉 Instead of step-by-step function calls,
👉 Execution happens as a coordinated graph process driven by state and message passing :


==============================================================
1. THREE-PHASE LIFECYCLE
==============================================================

A LangGraph workflow moves through three main phases:

--------------------------------------------------------------

A. Graph Definition

You define:

    - Nodes → tasks (functions, LLM calls, tools)
    - Edges → control flow (order, branching, loops)
    - State → shared memory (TypedDict / schema)

👉 This is the DESIGN phase


--------------------------------------------------------------

B. Compilation

Before execution, the graph is compiled:

    graph = builder.compile()

• Validates structure:
    - No disconnected (orphan) nodes
    - Proper edge connections
    - Logical consistency

👉 Ensures the workflow is correct BEFORE running


--------------------------------------------------------------

C. Execution (Invocation)

Execution starts with:

    graph.invoke(initial_state)

• Initial state is injected
• First node(s) are triggered

👉 This kicks off the runtime execution


==============================================================
2. NODE ACTIVATION & MESSAGE PASSING
==============================================================

Execution is driven by nodes reacting to state.

--------------------------------------------------------------

A. Node Activation

• A node is triggered when it receives state
• Its Python function executes

--------------------------------------------------------------

B. Partial State Update

• Node does NOT rebuild full state
• It returns only updates:

    return {"key": new_value}

👉 This is called a "partial update"


--------------------------------------------------------------

C. Message Passing

• Updated state flows automatically via edges
• Next node(s) receive updated state

👉 No manual data passing required


==============================================================
3. SUPERSTEPS (CORE EXECUTION UNIT)
==============================================================

LangGraph executes in rounds called SUPERSTEPS.

--------------------------------------------------------------

A. Why Supersteps?

Because multiple nodes can run in parallel

Example:
    Node A → triggers B, C, D simultaneously

--------------------------------------------------------------

B. Parallel Execution

• All active nodes in a round execute together

--------------------------------------------------------------

C. Aggregation via Reducers

• If multiple nodes update same key:
    → Reducers merge results

👉 Ensures consistent state after parallel execution


--------------------------------------------------------------

D. Iterative Rounds

Execution proceeds:

    Superstep 1 → Superstep 2 → Superstep 3 → ...

Until completion


==============================================================
4. TERMINATION (STOPPING CONDITION)
==============================================================

Execution stops automatically when:

1. No active nodes remain
2. No further state/messages are flowing

👉 Graph reaches END (natural completion)


==============================================================
🔥 FINAL INTUITION
==============================================================

Traditional Programming:
    You manually:
        → Call functions
        → Pass data
        → Control flow

LangGraph:
    System automatically:
        → Activates nodes
        → Passes state
        → Manages execution rounds

--------------------------------------------------------------

Superstep Model:
    "Run everything that can run → merge → repeat"


==============================================================
📌 CORE MENTAL MODEL
==============================================================

Graph = Execution Engine

State = Data flowing through system

Nodes = Workers processing data

Edges = Routing logic

Supersteps = Execution cycles

--------------------------------------------------------------

👉 You DESIGN the workflow
👉 LangGraph EXECUTES it automatically
"""