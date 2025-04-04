from pydantic import BaseModel
from llm.openai_llm import OpenAI_LLM
from llm.anthropic_llm import Anthropic_LLM
from fastapi import FastAPI, HTTPException
import os
from dotenv import load_dotenv
load_dotenv()

llm_type = os.getenv("LLM_TYPE", "anthropic")
if llm_type == "openai":
    llm = OpenAI_LLM()
elif llm_type == "anthropic":
    llm = Anthropic_LLM()
else:
    raise ValueError("Unsupported LLM type.")

class QueryRequest(BaseModel):
    query: str


app = FastAPI()

@app.post("/get_result")
def nl_to_sql(request: QueryRequest):
    try:
        result = llm.get_result(request.query)
        return {"data": result.get('result')}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



