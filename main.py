import asyncio
import json
import aiohttp
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

class Block(BaseModel):
    # Define your Block model here
    pass

async def fetch_blocks():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://polkadot-be.onrender.com/blocks') as response:
            return await response.json()

@app.get("/blocks")
async def read_blocks():
    blocks = await fetch_blocks()
    return blocks

if __name__ == "__main__":
    run(app, host="localhost", port=8000)
