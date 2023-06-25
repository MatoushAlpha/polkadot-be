import asyncio
import json
import websockets
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from uvicorn import run
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app = FastAPI()

@app.get("/blocks")
async def read_blocks():
    with open('blocks.json', 'r') as f:
        return json.load(f)

if __name__ == "__main__":
    run(app, host="localhost", port=8000)
