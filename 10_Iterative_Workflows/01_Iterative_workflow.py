"""
LangGraph Iterative Workflow (Generate → Evaluate → Improve → Loop)

Flow:
START → generate → evaluate → (approved → END)
                                 ↓
                          (needs_improvement)
                                 ↓
                              optimize
                                 ↓
                              evaluate → loop
"""

# ================================
# Imports
# ================================
from typing import TypedDict, Literal, Annotated, List
from langgraph.graph import StateGraph, START, END
from langchain_ollama import ChatOllama
import operator


# ================================
# Initialize LLMs (Ollama)
# ================================
generator_llm = ChatOllama(model="llama3.1:8b", temperature=0.7)
evaluator_llm = ChatOllama(model="llama3.1:8b", temperature=0)
optimizer_llm = ChatOllama(model="llama3.1:8b", temperature=0.7)


# ================================
# Define State
# ================================
class TweetState(TypedDict):
    topic: str
    tweet: str

    evaluation: Literal["approved", "needs_improvement"]
    feedback: str

    iteration: int
    max_iteration: int

    # Optional history (Reducer: append)
    tweet_history: Annotated[List[str], operator.add]
    feedback_history: Annotated[List[str], operator.add]


# ================================
# Node 1: Generate Tweet
# ================================
def generate_tweet(state: TweetState) -> dict:
    prompt = f"""
    Write a short, funny, viral tweet on:
    {state['topic']}

    Rules:
    - Max 280 characters
    - No Q&A format
    - Use simple, relatable humor
    """

    tweet = generator_llm.invoke(prompt).content

    return {
        "tweet": tweet,
        "tweet_history": [tweet]
    }


# ================================
# Node 2: Evaluate Tweet
# ================================
def evaluate_tweet(state: TweetState) -> dict:
    prompt = f"""
    Evaluate this tweet:

    "{state['tweet']}"

    Criteria:
    - Funny?
    - Original?
    - Short and punchy?

    Respond ONLY with:
    approved OR needs_improvement

    Also give 1 short feedback line.
    """

    response = evaluator_llm.invoke(prompt).content.lower()

    # Simple parsing (kept clean intentionally)
    if "approved" in response:
        evaluation = "approved"
    else:
        evaluation = "needs_improvement"

    return {
        "evaluation": evaluation,
        "feedback": response,
        "feedback_history": [response]
    }


# ================================
# Node 3: Optimize Tweet
# ================================
def optimize_tweet(state: TweetState) -> dict:
    prompt = f"""
    Improve this tweet using feedback:

    Tweet:
    {state['tweet']}

    Feedback:
    {state['feedback']}

    Make it funnier, sharper, and viral.
    """

    improved_tweet = optimizer_llm.invoke(prompt).content

    return {
        "tweet": improved_tweet,
        "iteration": state["iteration"] + 1,
        "tweet_history": [improved_tweet]
    }


# ================================
# Routing Logic (Loop Control)
# ================================
def route_evaluation(state: TweetState) -> str:
    # Stop if approved OR max iterations reached
    if state["evaluation"] == "approved" or state["iteration"] >= state["max_iteration"]:
        return "END"
    else:
        return "optimize"


# ================================
# Build Graph
# ================================
builder = StateGraph(TweetState)

# Nodes
builder.add_node("generate", generate_tweet)
builder.add_node("evaluate", evaluate_tweet)
builder.add_node("optimize", optimize_tweet)

# Flow
builder.add_edge(START, "generate")
builder.add_edge("generate", "evaluate")

# Conditional loop
builder.add_conditional_edges(
    "evaluate",
    route_evaluation,
    {
        "optimize": "optimize",
        "END": END
    }
)

# Loop back
builder.add_edge("optimize", "evaluate")

# Compile
graph = builder.compile()


# ================================
# Execute
# ================================
initial_state = {
    "topic": "Indian Railways",
    "tweet": "",
    "evaluation": "needs_improvement",
    "feedback": "",
    "iteration": 0,
    "max_iteration": 5,
    "tweet_history": [],
    "feedback_history": []
}

result = graph.invoke(initial_state)

print("\n=== FINAL TWEET ===\n")
print(result["tweet"])

print("\n=== ITERATIONS ===", result["iteration"])


"""
LangGraph Iterative Workflow (Generate → Evaluate → Improve → Loop)

Purpose
-------
Build a self-improving AI pipeline where output is refined
through feedback until it meets quality criteria or a limit is reached.

Flow:
START → generate → evaluate → (approved → END)
                                 ↓
                          (needs_improvement)
                                 ↓
                              optimize
                                 ↓
                              evaluate → loop


------------------------------------------------------------
1️⃣ State (Core of the System)
------------------------------------------------------------

class TweetState(TypedDict):
    topic: str
    tweet: str
    evaluation: "approved" | "needs_improvement"
    feedback: str
    iteration: int
    max_iteration: int
    tweet_history: List[str]
    feedback_history: List[str]

State acts as shared memory across all nodes.

Fields explained:
• topic → input idea (e.g., "Indian Railways")
• tweet → current version of generated output
• evaluation → decision from evaluator
• feedback → reason for improvement
• iteration → current loop count
• max_iteration → safety limit to avoid infinite loops

History fields:
• tweet_history → stores all versions of tweet
• feedback_history → stores all feedback

These are important for:
✔ debugging
✔ tracking improvement
✔ auditability


------------------------------------------------------------
2️⃣ Reducers (VERY IMPORTANT)
------------------------------------------------------------

tweet_history: Annotated[List[str], operator.add]
feedback_history: Annotated[List[str], operator.add]

Default behavior:
❌ overwrite old values

With reducer (operator.add):
✔ append new values to list

Example:
["tweet1"] + ["tweet2"] → ["tweet1", "tweet2"]

This allows:
✔ full iteration tracking
✔ no data loss across steps


------------------------------------------------------------
3️⃣ Node 1 → generate_tweet
------------------------------------------------------------

Input:
• topic

Process:
• LLM generates a tweet based on rules:
  - max 280 chars
  - funny, viral
  - simple language

Output:
{
    "tweet": generated_text,
    "tweet_history": [generated_text]
}

Key idea:
✔ First draft generation
✔ Starts the pipeline


------------------------------------------------------------
4️⃣ Node 2 → evaluate_tweet
------------------------------------------------------------

Input:
• tweet

Process:
• LLM evaluates based on:
  - humor
  - originality
  - brevity

Output:
{
    "evaluation": "approved" OR "needs_improvement",
    "feedback": "...",
    "feedback_history": [feedback]
}

Important:
✔ This is the "critic" node
✔ Drives the improvement loop


------------------------------------------------------------
5️⃣ Node 3 → optimize_tweet
------------------------------------------------------------

Input:
• tweet + feedback

Process:
• LLM improves tweet using feedback
• Makes it sharper, funnier, more engaging

Output:
{
    "tweet": improved_tweet,
    "iteration": iteration + 1,
    "tweet_history": [improved_tweet]
}

Key idea:
✔ Uses feedback to refine output
✔ Increments iteration count


------------------------------------------------------------
6️⃣ Routing Logic (Loop Control)
------------------------------------------------------------

def route_evaluation(state):

Condition 1:
✔ If evaluation == "approved" → STOP

Condition 2:
✔ If iteration >= max_iteration → STOP

Else:
✔ Continue → optimize

Why needed:
• Prevent infinite loops
• Ensure bounded execution


------------------------------------------------------------
7️⃣ Graph Structure
------------------------------------------------------------

START → generate → evaluate
                 ↙        ↘
             END       optimize
                          ↓
                       evaluate (loop)

• evaluate acts as decision point
• optimize feeds back into evaluate


------------------------------------------------------------
8️⃣ Execution Walkthrough
------------------------------------------------------------

Initial Input:
topic = "Indian Railways"
iteration = 0

Step 1:
generate → tweet_v1

Step 2:
evaluate → needs_improvement + feedback

Step 3:
optimize → tweet_v2, iteration=1

Step 4:
evaluate → maybe still needs improvement

Loop continues...

Final:
✔ either approved
✔ or max_iteration reached

Output:
• best tweet
• full history of attempts


------------------------------------------------------------
9️⃣ Multi-LLM Design (Separation of Roles)
------------------------------------------------------------

generator_llm  → creative generation  
evaluator_llm  → strict evaluation (low temp)  
optimizer_llm  → creative refinement  

Why separate?

✔ better control
✔ clearer responsibilities
✔ improved output quality


------------------------------------------------------------
🔟 Key Design Patterns Used
------------------------------------------------------------

✔ Iterative refinement (feedback loop)  
✔ Conditional routing (dynamic graph path)  
✔ State accumulation (history tracking)  
✔ Multi-agent style separation (generator/evaluator/optimizer)  


------------------------------------------------------------
11️⃣ Real-World Applications
------------------------------------------------------------

This pattern is used in:

• Code generation + review systems  
• Content optimization pipelines  
• AI agents with self-correction  
• RL-style feedback loops  
• Prompt refinement systems  

------------------------------------------------------------
Key Takeaway
------------------------------------------------------------

This is a "self-correcting AI system":

Generate → Evaluate → Improve → Repeat

LangGraph enables:
✔ controlled loops
✔ dynamic routing
✔ memory across iterations

This is a core pattern for building advanced AI agents.
"""
