from fastapi import APIRouter
from pydantic import BaseModel
from app.services.nlp import parse_query

router = APIRouter()

class QueryRequest(BaseModel):
    text: str

@router.post("/query")
async def process_query(req: QueryRequest):
    result = parse_query(req.text)
    if result["intent"] == "out_of_scope":
        return {"message": "I didn't understand. Try: 'recommend a warm beach trip'"}
    return result