"""
PROBLEM: "Glue Code" in LangChain vs Solution in LangGraph

--------------------------------------------------------
🔴 THE PROBLEM IN LANGCHAIN
--------------------------------------------------------

LangChain is primarily designed for linear workflows ("chains"),
which makes handling complex logic difficult.

1. Manual Stitching (Glue Code)
   - Developers must write custom Python logic:
     - while loops
     - if-else conditions
   - Used to connect different steps manually

2. Maintenance Issues
   - As complexity increases:
       → Glue code increases
       → Code becomes messy and hard to debug
       → Difficult to scale

3. Statelessness
   - Chains do not maintain shared state
   - Developer must manually:
       → Pass data between steps
       → Track intermediate outputs

👉 Result:
   Business Logic + Control Logic + State Handling = Mixed (Messy)


--------------------------------------------------------
🟢 HOW LANGGRAPH SOLVES THIS
--------------------------------------------------------

LangGraph introduces a graph-based orchestration model.

1. Native Logical Constructs
   - Workflow = Graph
       → Nodes = Tasks
       → Edges = Flow
   - Supports:
       → Conditional branching
       → Loops (via edges)
       → Dynamic routing

2. Zero (or Near-Zero) Glue Code
   - No need for:
       → while loops
       → if-else flow control in main logic
   - Flow is defined declaratively in graph

3. Stateful Execution
   - Shared state object (dictionary)
   - Automatically passed between nodes
   - No manual data passing required

4. Built-in Orchestration
   - Handles:
       → Execution order
       → Routing
       → Retries
       → Transitions

👉 Result:
   Business Logic ONLY in nodes
   Orchestration handled by LangGraph


--------------------------------------------------------
🔥 CORE DIFFERENCE (INTUITION)
--------------------------------------------------------

LangChain:
    You write EVERYTHING
    (logic + flow + state + connections)

LangGraph:
    You write ONLY logic
    (graph handles flow + state + orchestration)


--------------------------------------------------------
🚀 FINAL TAKEAWAY
--------------------------------------------------------

LangChain:
    Good for simple, linear workflows

LangGraph:
    Designed for complex, production-grade systems
    (loops, agents, multi-step reasoning, orchestration)

--------------------------------------------------------
📌 NOTE (Important Precision)
--------------------------------------------------------

"Zero glue code" ≠ literally zero lines

It means:
    Glue code is NOT written manually
    It is absorbed into the graph abstraction

--------------------------------------------------------
"""