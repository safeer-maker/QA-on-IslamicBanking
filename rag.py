from dotenv import load_dotenv
import os
from db_vector import vector_db
from logger import *
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import config,  json
load_dotenv()

class rag_class():
    def __init__(self):
        self.llm = ChatOpenAI (model=config.llm_model)
        self.db = vector_db()
        # self.prompt = PromptTemplate()
        self.input_question = ""
        self.related_questions = []
        self.related_data = []
        self.context = []
        log_info({"class": "rag", "method": "__init__", "message": "rag class object created"})

    def llm_invoke(self, prompt: str):
        return self.llm.invoke (prompt)
    
    def prompt_template_multi_questions (self, input_question : str , no_of_questions : int = 5):
      
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

      prompt = PromptTemplate.from_template(
          prompt_template
        ).format(
            question=input_question,
            no_of_questions = no_of_questions
            )
      log_info({"class": "rag", "method": "prompt_template_multi_questions", "prompt": prompt})
      return prompt

    def format_context (self, related_questions):
        doc = "Context: \n\n"
        for i in related_questions:
            doc += "Passage : " + i + "\n\n"
        return doc
    
    def prompt_template_multi_query_rag (self, context: str):
      
      prompt_template = """You are an AI model designed to answer questions based on retrieved context from a knowledge base. You will be given an input question and a set of context passages retrieved based on that question. Your task is to synthesize information from these context passages to provide a coherent, accurate, and concise answer to the input question.

      Instructions:

      Understand the Input Question: Carefully read the input question to determine what specific information is being asked.
      
      Analyze the Context Passages: Examine the context passages provided. Identify the most relevant information that directly addresses the input question.
      
      Synthesize the Information: Combine relevant information from multiple context passages if necessary to form a complete and accurate answer.
      
      Answer the Question: Write a response that directly answers the input question. Ensure that your answer is clear, concise, and well-supported by the context provided. If the context provided is insufficient to answer the question, you may indicate that more information is needed or tell answer insufficent data to answer this question.
      
      Input:
      Question: {input_question}

      {context} 
      """

      prompt = PromptTemplate.from_template (
          prompt_template
        ).format(
          input_question  = self.input_question,
          context         = context
        )
      log_info({"class": "rag", "method": "prompt_template_multi_query_rag", "prompt": prompt})
      return prompt

    def get_related_questions (self, input_question, no_of_questions : int = 5):
        prompt = self.prompt_template_multi_questions(input_question, no_of_questions)
        response = self.llm_invoke (prompt)
        multi_ques = json.loads  (response.content)
        self.related_questions = multi_ques['related_questions']
        self.related_questions.insert(0, input_question)
        log_info({"class": "rag", "method": "get_related_questions", "related_questions": self.related_questions})
        return self.related_questions

    def get_related_data (self, related_questions,  query_doc_per_question: int):
        
        for i in related_questions:
            self.related_data.extend ( self.db.db_query(i, num_results = query_doc_per_question)["documents"][0] )
        log_info({"class": "rag", "method": "get_related_data", "related_data": self.related_data})
        return self.related_data

    def remove_dublicate (self, related_data):
        self.no_dublicate = list(set(related_data))
        return self.no_dublicate

    def get_rag (self, input_question, no_of_questions : int):
        log_info({"class": "rag", "method": "get_rag", "input_question": input_question, "no_of_questions": no_of_questions})
        self.related_questions = self.get_related_questions(input_question , no_of_questions)
        self.related_data = self.get_related_data(self.related_questions, config.query_doc_per_question)
        context = self.remove_dublicate(self.related_data)
        self.context = self.format_context (context)
        return self.context
    
    def rag_base_answer (self, input_question : str ):
        if input_question == '':
            log_critical({"class": "rag", "method": "rag_base_answer", "message": "No input question"})
            return "No input question"
        
        self.input_question = input_question
        self.get_rag (self.input_question, config.no_of_questions)
        
        prompt = self.prompt_template_multi_query_rag (self.context)
        answer = self.llm_invoke (prompt=prompt).content
        log_info ({"class": "rag", "method": "rag_base_answer", "answer": answer})
        return answer


if __name__ == "__main__":
    rag = rag_class()
    print (rag.rag_base_answer("what is islamic banking") )



