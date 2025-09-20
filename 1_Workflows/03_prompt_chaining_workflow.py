from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from dotenv import load_dotenv

load_dotenv()

# create a model
model =  ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2)

# defining state 
class BLOGState(TypedDict):
    topic: str
    outline : str
    blog: str


# defing node
def generate_outline(state: BLOGState) -> BLOGState:

    topic = state["topic"]
    prompt = f"Generate a detailed outline for a blog on the topic -{topic}"
    outline = model.invoke(prompt).content
    state["outline"] = outline
    return state

def generate_blog(state: BLOGState) -> BLOGState:

    topic = state["topic"]
    outline = state["outline"]
    prompt = f"write a detailed blog on given topic:{topic} and given outline: {outline}"
    blog = model.invoke(prompt).content
    state["blog"] = blog
    return state

# defining a graph
graph = StateGraph(BLOGState)


# Adding Nodes, Edges and compile Graph  
graph.add_node("generate_outline", generate_outline)
graph.add_node("generate_blog", generate_blog)

graph.add_edge(START, "generate_outline")
graph.add_edge("generate_outline","generate_blog")
graph.add_edge("generate_blog", END)

workflow = graph.compile()

# exicurte the graph
state = {"topic": "Agentic AI"}

result = workflow.invoke(state)

print(result["blog"])


