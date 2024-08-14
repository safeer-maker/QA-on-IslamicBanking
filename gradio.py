import gradio as gr
import requests
import config

# Replace with your API endpoint
API_URL = f"http://{config.db_url}:{config.api_port}"

def query_db(query):
    response = requests.get(f"{API_URL}/db-query/{query}")
    if response.status_code == 200:
        return response.json()
    else:
        return "Error querying DB"

def reset_db():
    response = requests.get(f"{API_URL}/reset/db")
    return response.json()

def reset_pdf():
    response = requests.get(f"{API_URL}/reset/pdf")
    return response.json()

def add_db():
    response = requests.get(f"{API_URL}/add_db")
    return response.json()

def question_answer(query):
    response = requests.get(f"{API_URL}/question-answer-from-data/{query}")
    if response.status_code == 200:
        return response.json()['answer']
    else:
        return "Error answering question"

# Gradio Interface
def gradio_app():
    with gr.Blocks() as demo:
        with gr.Row():
            db_query_input = gr.Textbox(label="DB Query")
            db_query_output = gr.Textbox(label="Query Result", interactive=False)
            db_query_button = gr.Button("Query DB")

        with gr.Row():
            question_input = gr.Textbox(label="Question")
            answer_output = gr.Textbox(label="Answer", interactive=False)
            question_button = gr.Button("Ask Question")

        with gr.Row():
            reset_db_button = gr.Button("Reset DB")
            reset_pdf_button = gr.Button("Reset PDF")
            add_db_button = gr.Button("Add DB Data")

        # Button actions
        db_query_button.click(fn=query_db, inputs=db_query_input, outputs=db_query_output)
        question_button.click(fn=question_answer, inputs=question_input, outputs=answer_output)
        reset_db_button.click(fn=reset_db, outputs=None)
        reset_pdf_button.click(fn=reset_pdf, outputs=None)
        add_db_button.click(fn=add_db, outputs=None)

    return demo

if __name__ == "__main__":
    gradio_app().launch()
