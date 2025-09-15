from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
load_dotenv()


llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2)

response = llm.invoke("what is machine learnig")

print(response.content)