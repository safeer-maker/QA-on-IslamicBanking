from fastapi import FastAPI
from db_vector import vector_db
import config
from rag import rag_class

import uvicorn

app = FastAPI()
db = vector_db()
rag = rag_class()
print ("itemns in DB : ", db.collection.count())

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/db-query/{query}")
async def query(query: str):
    result = db.db_query(query)
    return result['documents']

@app.get("/reset/db")
async def reset_db():
    db.db_del()
    return {"message": "DB Reset"}

@app.get("/reset/pdf")
async def reset_pdf():
    db.def_pdf_list()
    return {"message": "PDF Reset"}

# @app.get("/reset/zip")
# async def reset_zip():
#     db.def_zip_list()
#     return {"message": "ZIP Reset"}

@app.get ('/add_db')
async def add_db():
    db.db_extract_add()
    return {"message": "data added to DB"}

@app.get ('/question-answer-from-data/{query}')
async def question_answer_from_data(query: str):
    
    answer = rag.rag_base_answer(query)
    return {"answer": answer}

if __name__ == "__main__":
    uvicorn.run( app, port = config.api_port)
