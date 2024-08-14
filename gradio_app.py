import gradio as gr
import requests
import config

url = f"{config.api_url}:{config.api_port}"

def search(query):
    response = requests.get(f"{url}/db-query/{query}")
    return response.json()

def reset_db():
    response = requests.get(f"{url}/reset/db")
    return response.json()

def reset_pdf():
    response = requests.get(f"{url}/reset/pdf")
    return response.json()

def add_data_to_db():
    response = requests.get(f"{url}/add_db")
    return response.json()

def question_answer(query):
    response = requests.get(f"{url}/question-answer-from-data/{query}")
    return response.json()

demo = gr.Blocks()

with demo:
    gr.Markdown("# FastAPI Demo")
    query = gr.Textbox(label="Query", placeholder="Enter your query")
    result = gr.JSON(label="Results")
    answer = gr.Textbox(label="Answer")

    search_button = gr.Button("Search")
    search_button.click(search, inputs=[query], outputs=[result])

    reset_db_button = gr.Button("Reset DB")
    reset_db_button.click(reset_db, inputs=[], outputs=[result])

    reset_pdf_button = gr.Button("Reset PDF")
    reset_pdf_button.click(reset_pdf, inputs=[], outputs=[result])

    add_data_to_db_button = gr.Button("Add Data to DB")
    add_data_to_db_button.click(add_data_to_db, inputs=[], outputs=[result])

    question_answer_button = gr.Button("Question Answer")
    question_answer_button.click(question_answer, inputs=[query], outputs=[answer])

demo.launch()