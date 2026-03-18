from fastapi import FastAPI
from pydantic import BaseModel
from api import explain_code_payload

app = FastAPI(title="Python Code Explainer API")


class CodeRequest(BaseModel):
    code: str


@app.get("/")
def root():
    return {"message": "Python Code Explainer API is running"}


@app.post("/explain")
def explain_code(request: CodeRequest):
    return explain_code_payload(request.code)