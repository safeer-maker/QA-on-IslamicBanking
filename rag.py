from dotenv import load_dotenv
import os

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import config,  json

load_dotenv()

llm = ChatOpenAI (model=config.llm_model)

input_question = "what is llm"

prompt_template = """
You are an AI assistant that generates multiple related questions based on an input question. Your task is to take the given question and create a series of connected questions that explore different aspects of the topic. The output should be in dictionary format.

**Input Question:** 
{question}

**Output:**
Provide a python dictonary object with the following structure:
dict (
  "original_question": "<question>",
  "related_questions": [
    "<related_question_1>",
    "<related_question_2>",
    "<related_question_3>",
    ...
  ]
)
"""

prompt = prompt_template.format(question=input_question)

print (prompt)

response = llm.invoke (prompt)

print (response)

multi_question =  ["Can you explain the concept of llm?","What does llm stand for and how is it used?", "How is llm defined and what are its applications?","Could you provide information on the meaning and significance of llm?", "In what context is llm commonly used and what are its key features?"]

multi_ques =   json.loads  (response.content)

print (multi_ques)


