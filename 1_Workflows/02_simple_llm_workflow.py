from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import START, END, StateGraph
from typing import TypedDict
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2)

# defining state
class LLMState(TypedDict):
    question: str
    answer: str

# defing llm node
def chatbot(state: LLMState) -> LLMState:
    # extract the question from state
    question = state['question']

    # form a prompt
    prompt = f'Answer the following question {question}'

    # ask that question to the LLM
    answer = model.invoke(prompt).content

    # update the answer in the state
    state['answer'] = answer

    return state

# defining the graph
graph = StateGraph(LLMState)

# adding nodes
graph.add_node("chatbot", chatbot)

graph.add_edge(START, "chatbot")
graph.add_edge("chatbot", END)

workflow = graph.compile()

# exicute the graph
state = {"question": "How far is moon from the earth?"}
result = workflow.invoke(state)

print(result["answer"])