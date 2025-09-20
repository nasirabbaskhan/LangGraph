from langgraph.graph import StateGraph, START, END
from typing import TypedDict



# Defining state
class Batsmantate(TypedDict):
    runs: int
    balls: int
    fours: int
    sixes: int

    strike_rate: float
    runs_in_boundery_persentage: float
    boundery_per_balls_persentage: float
    summary: str

# defining nodes
def calculate_strike_rate(state: Batsmantate) -> Batsmantate:
    runs = state["runs"]
    balls = state["balls"]
    # calculate strike rate
    sr = (runs/balls)*100

    return {"strike_rate": sr}



def calculate_boundery_persentage(state: Batsmantate):
    runs = state["runs"]
    fours = state["fours"]
    sixes = state["sixes"]

    # calculate boundery_persentage
    score_by_bounderies =  (fours * 4 + sixes * 6)
    boundery_persentage = (score_by_bounderies/runs)*100
    # boundary_percent = (((state['fours'] * 4) + (state['sixes'] * 6))/state['runs'])*100

    return {"runs_in_boundery_persentage": boundery_persentage}


def calculate_boundery_per_balls_persentage(state: Batsmantate):

    bpb = ((state['fours'] + state['sixes'])/state["balls"])*100

    return {"boundery_per_balls_persentage": bpb}

def generate_summary(state: Batsmantate):
    summary = f"""
Strike Rate - {state['strike_rate']} \n
Boundary percent - {state['runs_in_boundery_persentage']} \n
Balls per boundary - {state['boundery_per_balls_persentage']} 

"""
    
    return {'summary': summary}



# Defining grapg
graph = StateGraph(Batsmantate)

# Adding nodes and adges
graph.add_node("calculate_strike_rate", calculate_strike_rate)
graph.add_node("calculate_boundery_persentage", calculate_boundery_persentage)
graph.add_node("calculate_boundery_per_balls_persentage", calculate_boundery_per_balls_persentage)
graph.add_node("generate_summary", generate_summary)

graph.add_edge(START, "calculate_strike_rate")
graph.add_edge(START, "calculate_boundery_persentage")
graph.add_edge(START, "calculate_boundery_per_balls_persentage")

graph.add_edge("calculate_strike_rate", "generate_summary")
graph.add_edge("calculate_boundery_persentage", "generate_summary")
graph.add_edge("calculate_boundery_per_balls_persentage", "generate_summary")

graph.add_edge("generate_summary", END)

# compile the graph
workflow = graph.compile()

# exicute the graph
state = { "runs": 100, "balls": 50, "fours": 6, "sixes": 4}

result = workflow.invoke(state)

print(result)