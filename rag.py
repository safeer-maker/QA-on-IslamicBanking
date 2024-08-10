from dotenv import load_dotenv
import os
from db_vector import vector_db

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
Provide a python dictonary object with the following structure.\
  don't write python code in the output:
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

# response = llm.invoke (prompt)
# print (response)
# multi_ques =   json.loads  (response.content)
# print (multi_ques)
sample_question_dict = {'original_question': 'what is llm?',
 'related_questions': ['What does LLM stand for?',
  'How does a large language model work?',
  'What are some comprint (multi_ques)mon applications of LLMs?',
  'What are the differences between LLMs and traditional machine learning models?',
  'What are the limitations of using LLMs?',
  'How are LLMs trained and what data do they require?',
  'What are some popular LLM frameworks or libraries?',
  'How do LLMs handle natural language understanding?',
  'What ethical considerations are associated with LLMs?',
  'What advancements have been made in LLM technology recently?']}


related_questions = sample_question_dict['related_questions']

db = vector_db()
# try:
#     # db = vector_db()
# except Exception as e:
#     print ("DB is down error code :", e)

related_data = []
for i in related_questions:
    related_data.extend (  db.db_query(i)["documents"][:] )

print (related_data)


