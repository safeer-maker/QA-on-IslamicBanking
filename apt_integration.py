from fastapi import FastAPI
from db_vector import vector_db

app = FastAPI()
cls = vector_db()
print ("itemns in DB : ", cls.collection.count())

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/query/{query}")
async def query(query: str):
    result = cls.db_query(query)
    return result['documents']

@app.get("/reset/db")
async def reset_db():
    cls.db_del()
    return {"message": "DB Reset"}

@app.get("/reset/pdf")
async def reset_pdf():
    cls.def_pdf_list()
    return {"message": "PDF Reset"}

@app.get ('/add_db')
async def add_db():
    cls.db_extract_add()
    return {"message": "data added to DB"}

