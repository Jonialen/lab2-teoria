# server_p2.py (server_p2.py)

from fastapi import FastAPI
from pydantic import BaseModel
import re
from fastapi.responses import JSONResponse

# Definimos el esquema del body
class RegexRequest(BaseModel):
    regex: str
    body: str

app = FastAPI()

@app.post("/match")
def match_regex(request: RegexRequest):
    try:
        pattern = re.compile(request.regex)
        match = bool(pattern.search(request.body))
        return {"match": match}
    except re.error as e:
        return JSONResponse(
            status_code=400,
            content={"error": f"Regex inválido: {str(e)}"}
        )
