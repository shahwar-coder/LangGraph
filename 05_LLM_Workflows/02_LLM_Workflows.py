"""
LLM WORKFLOWS — STRUCTURED EXPLANATION

An LLM workflow is a structured series of tasks executed to achieve a specific goal,
where multiple steps depend on Large Language Models (LLMs) for cognitive processes like:

    - reasoning
    - prompting
    - tool calling
    - decision-making

Unlike basic chatbots, workflows enable building complex, multi-step systems
by connecting modular components.


==============================================================
🔹 COMMON LLM WORKFLOW PATTERNS
==============================================================

1. PROMPT CHAINING (SEQUENTIAL)

A linear sequence of LLM calls where:
    Output of one step → Input to next step

Example:
    Topic → Outline → Detailed Report

Flow:
    LLM1 → LLM2 → LLM3


--------------------------------------------------------------

2. ROUTING (DECISION-BASED FLOW)

An LLM acts as a router/decision-maker:
    It analyzes input and selects the correct path

Example:
    User Query → Router LLM →
        → Refund Model
        → Tech Support Model
        → Sales Model

Key Idea:
    Dynamic path selection based on intent


--------------------------------------------------------------

3. PARALLELISATION (CONCURRENT EXECUTION)

A task is split into multiple sub-tasks:
    All executed simultaneously

Then:
    Results are combined (aggregated)

Example:
    Video Moderation:
        → Check toxicity
        → Check misinformation
        → Check policy violations

Key Idea:
    Faster + multi-aspect evaluation


--------------------------------------------------------------

4. ORCHESTRATOR–WORKER (DYNAMIC TASK BREAKDOWN)

An "Orchestrator" LLM:
    - Decides what sub-tasks are needed
    - Assigns them to workers

Unlike parallelisation:
    Tasks are NOT predefined

Example:
    Query →
        Orchestrator decides:
            → Use Google Scholar (scientific)
            → Use News API (political)

Key Idea:
    Dynamic decomposition of problems


--------------------------------------------------------------

5. EVALUATOR–OPTIMIZER (ITERATIVE LOOP)

Two LLM roles:

    Generator:
        Produces output

    Evaluator:
        Reviews output and gives feedback

Loop continues until:
    Output meets quality criteria

Example:
    Code generation → Review → Improve → Repeat

Key Idea:
    Refinement through feedback loop


==============================================================
🔹 WORKFLOWS vs AGENTS
==============================================================

WORKFLOWS:
    - Predefined structure
    - Fixed execution paths
    - Controlled by developer logic
    - Predictable behavior

AGENTS:
    - Dynamic decision-making
    - LLM decides next steps
    - Chooses tools autonomously
    - More flexible, less predictable


==============================================================
🔥 FINAL INTUITION
==============================================================

Workflow:
    "Follow a designed path"

Agent:
    "Figure out the path"

==============================================================
"""