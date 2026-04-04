# =========================
# 1. Imports
# =========================
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

# =========================
# 2. State
# =========================
class BMIState(TypedDict):
    weight_kg: float
    height_m: float
    bmi: float
    category: str  


# =========================
# 3. Node 1 → Calculate BMI
# =========================
def calculate_bmi(state: BMIState):
    bmi = state["weight_kg"] / (state["height_m"] ** 2)
    return {"bmi": round(bmi, 2)}  # ✅ partial update


# =========================
# 4. Node 2 → Label BMI
# =========================
def label_bmi(state: BMIState):
    bmi = state["bmi"]

    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"

    return {"category": category}  # ✅ partial update


# =========================
# 5. Build Graph
# =========================
builder = StateGraph(BMIState)

builder.add_node("calculate_bmi", calculate_bmi)
builder.add_node("label_bmi", label_bmi)

# Flow
builder.add_edge(START, "calculate_bmi")
builder.add_edge("calculate_bmi", "label_bmi")
builder.add_edge("label_bmi", END)

# =========================
# 6. Compile & Run
# =========================
graph = builder.compile()

result = graph.invoke({
    "weight_kg": 70,
    "height_m": 1.75
})

print(result)

# Output:
# {'weight_kg': 70, 'height_m': 1.75, 'bmi': 22.86, 'category': 'Normal'}


"""
LangGraph BMI Pipeline

Purpose
-------
Build a small workflow (graph) that:
1. Takes input (weight, height)
2. Calculates BMI
3. Classifies it into a category

This demonstrates how LangGraph manages state across steps.


------------------------------------------------------------
1️⃣ State (Shared Memory)
------------------------------------------------------------

class BMIState(TypedDict):
    weight_kg: float
    height_m: float
    bmi: float
    category: str

• This is the "shared state" flowing through the graph
• Each node reads from it and updates part of it
• Think of it as a mutable data object passed step-by-step


------------------------------------------------------------
2️⃣ Node 1 → calculate_bmi
------------------------------------------------------------

def calculate_bmi(state):
    bmi = weight / height²
    return {"bmi": value}

Key Idea:
• Reads → weight_kg, height_m
• Writes → bmi

Important:
• Returns ONLY updated fields (partial update)
• LangGraph merges it into global state

Before:
{weight, height}

After:
{weight, height, bmi}


------------------------------------------------------------
3️⃣ Node 2 → label_bmi
------------------------------------------------------------

def label_bmi(state):
    uses bmi → assigns category

• Reads → bmi
• Writes → category

Categories:
<18.5 → Underweight  
<25   → Normal  
<30   → Overweight  
else  → Obese


------------------------------------------------------------
4️⃣ Graph Construction
------------------------------------------------------------

builder = StateGraph(BMIState)

• Defines a workflow operating on BMIState

Nodes added:
calculate_bmi → label_bmi

Flow defined:

START → calculate_bmi → label_bmi → END

• Execution is strictly sequential here


------------------------------------------------------------
5️⃣ Execution Flow
------------------------------------------------------------

Input:
{
    "weight_kg": 70,
    "height_m": 1.75
}

Step 1:
calculate_bmi → adds bmi

Step 2:
label_bmi → adds category

Final Output:
{
    weight_kg,
    height_m,
    bmi,
    category
}


------------------------------------------------------------
6️⃣ Key Concept → Partial State Updates
------------------------------------------------------------

Each node returns ONLY what it computes:

calculate_bmi → {"bmi": ...}
label_bmi     → {"category": ...}

LangGraph automatically:
✔ merges updates
✔ preserves previous values

This avoids:
❌ overwriting full state
❌ passing unnecessary data manually


------------------------------------------------------------
7️⃣ Why This Pattern Matters
------------------------------------------------------------

This is how real AI pipelines work:

• Step 1 → preprocess
• Step 2 → analyze
• Step 3 → classify
• Step 4 → respond

Each step:
✔ independent
✔ reusable
✔ composable


------------------------------------------------------------
Key Takeaway
------------------------------------------------------------

LangGraph = controlled data flow + state updates

• State = shared memory
• Nodes = processing steps
• Edges = execution order

This creates clean, scalable pipelines for AI systems.
"""