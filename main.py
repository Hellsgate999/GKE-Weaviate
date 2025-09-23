# FastAPI Search API to connect with Weaviate
from fastapi import FastAPI, Query
import weaviate
import os

# Get Weaviate URL from env or fallback
WEAVIATE_URL = os.getenv("WEAVIATE_URL", "http://34.133.70.46:8080")

client = weaviate.Client(WEAVIATE_URL)
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Search API connected to Weaviate (v3 client)"}

@app.get("/get_all")
def get_all(class_name: str):
    try:
        result = client.query.get(class_name, ["question", "answer"]).do()
        return result
    except Exception as e:
        return {"error": str(e)}

@app.post("/insert")
def insert(class_name: str, question: str, answer: str):
    try:
        obj = {"question": question, "answer": answer}
        client.data_object.create(obj, class_name)
        return {"status": "inserted", "data": obj}
    except Exception as e:
        return {"error": str(e)}

@app.get("/search")
def search(class_name: str, q: str = Query(...)):
    try:
        response = client.query.get(class_name, ["question", "answer"]) \\
            .with_near_text({"concepts": [q]}).with_limit(3).do()
        return response
    except Exception as e:
        return {"error": str(e)}
