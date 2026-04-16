from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from typing import TypedDict


# ----------------------------
# STATE
# ----------------------------
class State(TypedDict):
    step1_done: bool
    step2_done: bool
    step3_done: bool


# ----------------------------
# NODE 1
# ----------------------------
def step_1(state: State):
    print("Running Step 1")
    return {"step1_done": True}


# ----------------------------
# NODE 2 (fails first time)
# ----------------------------
def step_2(state: State):
    print("Running Step 2")

    # simulate failure ONLY first time
    if not state.get("step2_done", False):
        print("❌ Simulating failure in Step 2...")
        raise Exception("Step 2 failed!")

    return {"step2_done": True}


# ----------------------------
# NODE 3
# ----------------------------
def step_3(state: State):
    print("Running Step 3")
    return {"step3_done": True}


# ----------------------------
# GRAPH
# ----------------------------
graph = StateGraph(State)

graph.add_node("step_1", step_1)
graph.add_node("step_2", step_2)
graph.add_node("step_3", step_3)

graph.add_edge(START, "step_1")
graph.add_edge("step_1", "step_2")
graph.add_edge("step_2", "step_3")
graph.add_edge("step_3", END)


# ----------------------------
# CHECKPOINTER
# ----------------------------
memory = InMemorySaver()
app = graph.compile(checkpointer=memory)


# ----------------------------
# RUN (demonstrates recovery)
# ----------------------------
if __name__ == "__main__":
    thread_id = "fault_demo"

    config = {"configurable": {"thread_id": thread_id}}

    print("\n--- First Run (will fail) ---\n")

    try:
        app.invoke({}, config=config)
    except Exception as e:
        print("Caught Error:", e)

    print("\n--- Second Run (resume) ---\n")

    # Fix state manually to simulate retry success
    # (In real case, you might fix bug / external issue)
    app.update_state(
        config,
        {"step2_done": True}
    )

    result = app.invoke({}, config=config)

    print("\nFinal State:", result)


# --- First Run (will fail) ---

# Running Step 1
# Running Step 2
# ❌ Simulating failure in Step 2...
# Caught Error: Step 2 failed!

# --- Second Run (resume) ---

# Running Step 1
# Running Step 2
# Running Step 3

# Final State: {'step1_done': True, 'step2_done': True, 'step3_done': True}