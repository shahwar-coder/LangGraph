"""
LangGraph Cricket Analytics Workflow

Flow:
START → (parallel metrics)
    → Strike Rate
    → Balls per Boundary
    → Boundary %
→ Summary → END
"""

# ================================
# Imports
# ================================
from typing import TypedDict
from langgraph.graph import StateGraph, START, END


# ================================
# Define State
# ================================
class BatsmanState(TypedDict):
    runs: int
    balls: int
    fours: int
    sixes: int

    sr: float
    bpb: float
    boundary_percent: float
    summary: str


# ================================
# Node 1: Strike Rate
# ================================
def calculate_sr(state: BatsmanState) -> dict:
    sr = (state["runs"] / state["balls"]) * 100
    return {"sr": sr}


# ================================
# Node 2: Balls per Boundary
# ================================
def calculate_bpb(state: BatsmanState) -> dict:
    boundaries = state["fours"] + state["sixes"]
    bpb = state["balls"] / boundaries if boundaries != 0 else 0
    return {"bpb": bpb}


# ================================
# Node 3: Boundary %
# ================================
def calculate_boundary_percent(state: BatsmanState) -> dict:
    boundary_runs = (state["fours"] * 4) + (state["sixes"] * 6)
    percent = (boundary_runs / state["runs"]) * 100 if state["runs"] != 0 else 0
    return {"boundary_percent": percent}


# ================================
# Node 4: Summary
# ================================
def generate_summary(state: BatsmanState) -> dict:
    summary = f"""
Strike Rate: {state['sr']:.2f}
Balls per Boundary: {state['bpb']:.2f}
Boundary %: {state['boundary_percent']:.2f}
"""
    return {"summary": summary}


# ================================
# Build Graph
# ================================
builder = StateGraph(BatsmanState)

# Add nodes
builder.add_node("calculate_sr", calculate_sr)
builder.add_node("calculate_bpb", calculate_bpb)
builder.add_node("calculate_boundary_percent", calculate_boundary_percent)
builder.add_node("summary", generate_summary)

# Parallel execution from START
builder.add_edge(START, "calculate_sr")
builder.add_edge(START, "calculate_bpb")
builder.add_edge(START, "calculate_boundary_percent")

# All converge to summary
builder.add_edge("calculate_sr", "summary")
builder.add_edge("calculate_bpb", "summary")
builder.add_edge("calculate_boundary_percent", "summary")

builder.add_edge("summary", END)

graph = builder.compile()


# ================================
# Execute
# ================================
initial_state = {
    "runs": 100,
    "balls": 50,
    "fours": 6,
    "sixes": 4,
    "sr": 0.0,
    "bpb": 0.0,
    "boundary_percent": 0.0,
    "summary": ""
}

result = graph.invoke(initial_state)

print("\n=== FINAL OUTPUT ===\n")
print(result["summary"])


"""
LangGraph Cricket Analytics Workflow

Purpose
-------
Compute multiple cricket performance metrics in parallel,
then combine them into a final summary.

Flow:
START → (parallel calculations) → summary → END


------------------------------------------------------------
1️⃣ State (Shared Data)
------------------------------------------------------------

class BatsmanState(TypedDict):
    runs, balls, fours, sixes
    sr, bpb, boundary_percent
    summary

• Input → runs, balls, fours, sixes
• Output → sr, bpb, boundary_percent, summary

State acts as shared memory across all nodes


------------------------------------------------------------
2️⃣ Parallel Nodes (Independent Calculations)
------------------------------------------------------------

Node 1 → Strike Rate
sr = (runs / balls) * 100

• Measures scoring speed
• Higher = faster scoring


Node 2 → Balls per Boundary (BPB)
bpb = balls / (fours + sixes)

• Measures how frequently boundaries occur
• Lower = more aggressive batting


Node 3 → Boundary %
boundary_runs = 4*fours + 6*sixes
percent = (boundary_runs / runs) * 100

• Measures how much scoring came from boundaries


Key Idea:
✔ These nodes do NOT depend on each other
✔ So they can run in parallel


------------------------------------------------------------
3️⃣ Parallel Execution (Important Concept)
------------------------------------------------------------

builder.add_edge(START, node1)
builder.add_edge(START, node2)
builder.add_edge(START, node3)

• All three nodes start at the same time
• Each reads the same input state
• Each writes its own field

LangGraph handles:
✔ parallel execution
✔ safe state merging


------------------------------------------------------------
4️⃣ Convergence → Summary Node
------------------------------------------------------------

All nodes connect to:

builder.add_edge(node1, "summary")
builder.add_edge(node2, "summary")
builder.add_edge(node3, "summary")

• Summary waits for ALL metrics
• Then combines results into readable output


------------------------------------------------------------
5️⃣ Summary Node
------------------------------------------------------------

def generate_summary(state):

• Reads:
    sr, bpb, boundary_percent

• Formats output:
    clean, readable report

Example Output:
Strike Rate: 200.00
Balls per Boundary: 5.00
Boundary %: 48.00


------------------------------------------------------------
6️⃣ Execution Flow
------------------------------------------------------------

Input:
runs=100, balls=50, fours=6, sixes=4

Step 1 (parallel):
✔ sr = 200
✔ bpb = 5
✔ boundary% ≈ 48

Step 2:
summary node combines results

Final Output:
state + computed metrics + summary


------------------------------------------------------------
7️⃣ Key Concept → Parallel Graphs
------------------------------------------------------------

Sequential:
A → B → C

Parallel:
      → A →
START → B → → Merge → END
      → C →

Benefits:
✔ faster execution
✔ independent computations
✔ clean modular design


------------------------------------------------------------
8️⃣ Why This Matters
------------------------------------------------------------

This pattern is used in:

• Analytics pipelines
• Feature engineering (ML)
• Multi-tool AI agents
• Monitoring systems

Any time:
✔ tasks are independent
✔ results need merging


------------------------------------------------------------
Key Takeaway
------------------------------------------------------------

LangGraph supports:

• Parallel computation (multiple nodes at once)
• Automatic state merging
• Clean separation of logic

This enables scalable, real-world data pipelines.
"""