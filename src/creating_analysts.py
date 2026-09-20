from src.utils.nodes import create_analysts , human_feedback
from langgraph.graph import START, END, StateGraph
from utils.states import GenerateAnalystsState
from dotenv import load_dotenv
from utils.edges import should_continue
load_dotenv()

# Creating our graph
builder = StateGraph(GenerateAnalystsState)

builder.add_node("create_analysts", create_analysts)
builder.add_node("human_feedback",human_feedback)

builder.add_edge(START, "create_analysts")
builder.add_edge("create_analysts", "human_feedback")

builder.add_conditional_edges(
    "human_feedback",
    should_continue,
    {
        "create_analysts": "create_analysts",
        "END": END,
    }
)
graph = builder.compile()