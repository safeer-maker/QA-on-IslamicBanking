from dotenv import load_dotenv
import os
from db_vector import vector_db

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import config,  json
load_dotenv()

class rag(vector_db):
    def __init__(self):
        self.llm = ChatOpenAI (model=config.llm_model)
        self.db = super().vector_db
        self.prompt = PromptTemplate()
        self.input_question = ""
        self.related_questions = []
        self.related_data = []
        self.no_dublicate = []

    def prompt_template (self, input_question, no_of_questions : int = 5):
      question = input_question
      prompt_template = """
        You are an AI assistant that generates multiple related questions based on an input question. Your task is to take the given question and create a series of connected questions that explore different aspects of the topic. The output should be in dictionary format.
        Number of generated question should not be more then {no_of_questions}.

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

      prompt = prompt_template.format(question=question , no_of_questions = no_of_questions)
      return prompt

    def format_context (self, related_questions):
        pass
    
    

    def get_related_questions (self, input_question, no_of_questions : int = 5):
        prompt = self.prompt_template(input_question, no_of_questions)
        response = self.llm.invoke (prompt)
        multi_ques = json.loads  (response.content)
        self.related_questions = multi_ques['related_questions']
        self.related_questions.insert(0, input_question)
        return self.related_questions

    def get_related_data (self, related_questions):
        for i in related_questions:
            self.related_data.extend ( self.db.db_query(i, num_results = 3)["documents"][0] )
        return self.related_data

    def remove_dublicate (self, related_data):
        self.no_dublicate = list(set(related_data))
        return self.no_dublicate

    def get_rag (self, input_question, no_of_questions : int):
        if no_of_questions is None:
            no_of_questions = config.no_of_questions

        related_questions = self.get_related_questions(input_question , no_of_questions)
        related_data = self.get_related_data(related_questions)
        no_dublicate = self.remove_dublicate(related_data)
        return no_dublicate

llm = ChatOpenAI (model=config.llm_model)

input_question = "what is llm"

prompt_template = """
You are an AI assistant that generates multiple related questions based on an input question. Your task is to take the given question and create a series of connected questions that explore different aspects of the topic. The output should be in dictionary format.
Number of generated question should not be more then 5.

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
    related_data.extend (  db.db_query(i, num_results = 3)["documents"][0] )

print (len (related_data))
no_dublicate = list(set(related_data))

print (len (no_dublicate))




