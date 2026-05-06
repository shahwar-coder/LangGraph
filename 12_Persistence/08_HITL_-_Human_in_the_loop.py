from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langgraph.graph.message import add_messages
from langchain_ollama import ChatOllama
from typing import TypedDict, Annotated


# ----------------------------
# STATE
# ----------------------------
class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    approved: bool


# ----------------------------
# LLM
# ----------------------------
llm = ChatOllama(model="mistral:7b", temperature=0.7)


# ----------------------------
# NODE 1: Generate LinkedIn Post
# ----------------------------
def generate_post(state: State):
    messages = state.get("messages", [])

    prompt = HumanMessage(content="""
Write a high-quality LinkedIn post on the given topic.
Keep it:
- concise
- engaging
- structured
- include a hook and bullet points if needed
""")

    response = llm.invoke(messages + [prompt])

    print("\n--- Generated LinkedIn Post ---\n")
    print(response.content)

    return {
        "messages": [prompt, response],
        "approved": False
    }


# ----------------------------
# NODE 2: Human Review (HITL)
# ----------------------------
def human_review(state: State):
    decision = input("\nApprove this post? (yes/no): ").strip().lower()

    if decision == "yes":
        return {"approved": True}
    else:
        return {"approved": False}


# ----------------------------
# ROUTER
# ----------------------------
def route(state: State):
    if state.get("approved"):
        return END
    return "generate_post"


# ----------------------------
# GRAPH
# ----------------------------
graph = StateGraph(State)

graph.add_node("generate_post", generate_post)
graph.add_node("human_review", human_review)

graph.add_edge(START, "generate_post")
graph.add_edge("generate_post", "human_review")

graph.add_conditional_edges("human_review", route)


# ----------------------------
# CHECKPOINTER
# ----------------------------
memory = InMemorySaver()
app = graph.compile(checkpointer=memory)


# ----------------------------
# RUN
# ----------------------------
if __name__ == "__main__":
    thread_id = "linkedin_post_session"

    topic = input("Enter topic for LinkedIn post: ")

    result = app.invoke(
        {"messages": [HumanMessage(content=topic)]},
        config={"configurable": {"thread_id": thread_id}}
    )

    print("\n✅ Final Approved Post:\n")
    print(result["messages"][-1].content)


# Enter topic for LinkedIn post: Agentic AI - boon or bane

# --- Generated LinkedIn Post ---

#  Title: Exploring the Frontier of Agentic AI: A Paradigm Shift in Technology 🔮🚀

# Hello Connections,

# I'm excited to dive into a fascinating topic that's been capturing the imagination of tech enthusiasts worldwide - Agentic AI. This post aims to shed light on what it is, why it matters, and its potential impact on our future.

# 🌐 Background: Traditional AI systems follow pre-defined rules or learn from data to make decisions. But Agentic AI takes a leap forward by empowering AI agents to act autonomously within a given environment, making them proactive rather than reactive.

# 🤔 Benefits: Agentic AI could revolutionize various sectors, including healthcare, finance, and transportation, through improved efficiency, faster decision-making, and personalized experiences. It can help doctors diagnose diseases earlier, financial advisors make smarter investments, and self-driving cars navigate complex traffic scenarios more effectively.

# 💡 Challenges: While Agentic AI holds great promise, it also raises ethical questions about accountability, privacy, and job displacement. As we develop these powerful agents, we must prioritize transparency, fairness, and responsible innovation to ensure a harmonious coexistence between humans and AI.

# 💭 Reflection: Are you curious about Agentic AI and its implications? Let's continue this conversation! Share your thoughts on how this technology could reshape our world or the challenges we might face as we embrace this new frontier.

# Looking forward to hearing your insights! 🚀🌐 #AgenticAI #ArtificialIntelligence #Innovation #FutureTech #EthicsInAI

# Approve this post? (yes/no): no

# --- Generated LinkedIn Post ---

#  Title: Empowering AI Agents: The Dawn of Agentic AI 🤖🌞

# Hello Connections,

# I'm thrilled to explore an exciting new frontier in AI development – Agentic AI! This technology is poised to revolutionize the way we interact with artificial intelligence and could reshape various industries.

# ✍️ What is Agentic AI? It's a next-generation AI system that empowers agents to act autonomously within a given environment, making decisions proactively rather than reactively. Think of it as self-driving cars that can adapt to unexpected road conditions or virtual assistants capable of understanding complex human emotions.

# 🎯 Benefits: Agentic AI promises increased efficiency, faster decision-making, and more personalized experiences across multiple sectors, such as healthcare, finance, and transportation. It could help doctors diagnose diseases earlier, financial advisors make smarter investments, and self-driving cars navigate complex traffic scenarios with ease.

# 🔍 Challenges: As Agentic AI gains traction, it raises ethical questions about accountability, privacy, and job displacement. Ensuring transparency, fairness, and responsible innovation will be crucial to create a harmonious coexistence between humans and AI.

# 💭 Reflection: What do you think about Agentic AI? How could this technology impact your industry or daily life? Share your thoughts on the opportunities and challenges it presents in the comments below! 🚀🌐 #AgenticAI #ArtificialIntelligence #Innovation #FutureTech #EthicsInAI

# Approve this post? (yes/no): yes

# ✅ Final Approved Post:

#  Title: Empowering AI Agents: The Dawn of Agentic AI 🤖🌞

# Hello Connections,

# I'm thrilled to explore an exciting new frontier in AI development – Agentic AI! This technology is poised to revolutionize the way we interact with artificial intelligence and could reshape various industries.

# ✍️ What is Agentic AI? It's a next-generation AI system that empowers agents to act autonomously within a given environment, making decisions proactively rather than reactively. Think of it as self-driving cars that can adapt to unexpected road conditions or virtual assistants capable of understanding complex human emotions.

# 🎯 Benefits: Agentic AI promises increased efficiency, faster decision-making, and more personalized experiences across multiple sectors, such as healthcare, finance, and transportation. It could help doctors diagnose diseases earlier, financial advisors make smarter investments, and self-driving cars navigate complex traffic scenarios with ease.

# 🔍 Challenges: As Agentic AI gains traction, it raises ethical questions about accountability, privacy, and job displacement. Ensuring transparency, fairness, and responsible innovation will be crucial to create a harmonious coexistence between humans and AI.

# 💭 Reflection: What do you think about Agentic AI? How could this technology impact your industry or daily life? Share your thoughts on the opportunities and challenges it presents in the comments below! 🚀🌐 #AgenticAI #ArtificialIntelligence #Innovation #FutureTech #EthicsInAI



"""
LangGraph HITL Workflow (Generate → Human Review → Loop)

Purpose
-------
Generate a LinkedIn post using an LLM and include a
Human-In-The-Loop (HITL) approval step before finalizing.

Flow:
START → generate_post → human_review → (approved → END)
                                           ↓
                                     (not approved)
                                           ↓
                                      generate_post (loop)


------------------------------------------------------------
1️⃣ State (with message memory)
------------------------------------------------------------

class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    approved: bool

• messages → conversation history (LLM + user + system)
• approved → decision flag from human

IMPORTANT:
add_messages (reducer)
✔ automatically appends new messages
✔ preserves full conversation context


------------------------------------------------------------
2️⃣ LLM Setup
------------------------------------------------------------

llm = ChatOllama(model="mistral:7b", temperature=0.7)

• temperature=0.7 → creative writing
• Suitable for content generation (LinkedIn posts)


------------------------------------------------------------
3️⃣ Node 1 → generate_post
------------------------------------------------------------

Input:
• previous messages (context)
• topic (first HumanMessage)

Process:
• Adds instruction prompt
• Calls LLM with full conversation

messages + [prompt] → LLM → response

Output:
{
    "messages": [prompt, response],
    "approved": False
}

Key Points:
✔ Uses full chat history (context-aware)
✔ Stores both prompt + response
✔ Resets approval to False


------------------------------------------------------------
4️⃣ Node 2 → human_review (HITL)
------------------------------------------------------------

Input:
• generated post (from messages)

Process:
• Asks human: approve? (yes/no)

Output:
{
    "approved": True / False
}

Key Idea:
✔ Human controls final decision
✔ Enables real-world validation


------------------------------------------------------------
5️⃣ Router (Decision Logic)
------------------------------------------------------------

def route(state):

if approved → END  
else → generate_post

• If approved → stop workflow
• If rejected → regenerate post

This creates a loop with human feedback


------------------------------------------------------------
6️⃣ Graph Structure
------------------------------------------------------------

START → generate_post → human_review
                         ↙        ↘
                      END    generate_post (loop)

• Loop continues until human approves


------------------------------------------------------------
7️⃣ Checkpointer (Memory Persistence)
------------------------------------------------------------

memory = InMemorySaver()
app = graph.compile(checkpointer=memory)

Purpose:
✔ Saves state between steps
✔ Enables thread-based sessions

thread_id:
"linkedin_post_session"

• Identifies a unique session
• Maintains conversation continuity


------------------------------------------------------------
8️⃣ Execution Flow
------------------------------------------------------------

Step 1:
User enters topic → stored as HumanMessage

Step 2:
generate_post → LLM creates post

Step 3:
human_review → user decides

If "no":
→ loop back → regenerate (with history)

If "yes":
→ END → final output


------------------------------------------------------------
9️⃣ Why add_messages Matters
------------------------------------------------------------

Without reducer:
❌ messages overwritten each step

With add_messages:
✔ messages accumulate
✔ LLM sees full history
✔ better iterations


------------------------------------------------------------
🔟 Why HITL is Important
------------------------------------------------------------

Used in real systems for:

• Content approval (marketing posts)
• Safety checks (AI outputs)
• Quality control
• Compliance workflows

Pattern:
AI generates → Human validates → AI improves


------------------------------------------------------------
Key Takeaway
------------------------------------------------------------

This is a Human-in-the-Loop system:

AI generates → Human reviews → Loop until approved

LangGraph enables:
✔ stateful conversations
✔ persistence via checkpointer
✔ human + AI collaboration workflows
"""