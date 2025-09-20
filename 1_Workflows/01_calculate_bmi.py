from langgraph.graph import StateGraph, START, END
from typing import TypedDict

# ********************************************** Defining state ***************************************

# defining state
class BMIState(TypedDict):
    weight_kg: float
    height_m: float
    bmi: float
    category: str

# ********************************************** Defining Nodes ***************************************

def calculate_bmi(state: BMIState)-> BMIState:
    weight = state["weight_kg"]
    height = state["height_m"]

    bmi = weight/(height**2)
    state["bmi"] = bmi # ubdate the bmi
    return state

def label_bmi(state: BMIState) -> BMIState:

    bmi = state['bmi']

    if bmi < 18.5:
        state["category"] = "Underweight"
    elif 18.5 <= bmi < 25:
        state["category"] = "Normal"
    elif 25 <= bmi < 30:
        state["category"] = "Overweight"
    else:
        state["category"] = "Obese"

    return state

# ********************************************** Defining Graph ***************************************

graph = StateGraph(BMIState)

# ********************************************** Adding Nods, Edges and compile Graph  *********************

# adding nodes in graph
graph.add_node('calculate_bmi', calculate_bmi)
graph.add_node('label_bmi', label_bmi)

# adding edges in graph
graph.add_edge(START, "calculate_bmi")
graph.add_edge("calculate_bmi", "label_bmi")
graph.add_edge("label_bmi", END)

# complile the graph
workflow = graph.compile()

# # ********************************** Exicute the Graph ***************************************

weight = float(input("Enter Weight in kg: "))
height = float(input("Enter height in m: "))
state = { "weight_kg": weight,
          "height_m": height
        }

result = workflow.invoke(state)

print(result)
print("calculated bmi: ",result["bmi"])
print("category bmi: ",result["category"])
