from src.utils.nodes import create_analysts
from langgraph.graph import START, END, StateGraph
from utils.states import GenerateAnalystsState
from dotenv import load_dotenv

load_dotenv()

# Creating our graph
builder = StateGraph(GenerateAnalystsState)

builder.add_node("create_analysts", create_analysts)

builder.add_edge(START, "create_analysts")
builder.add_edge("create_analysts", END)

graph = builder.compile()