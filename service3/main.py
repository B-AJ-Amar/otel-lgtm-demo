
from fastapi import FastAPI, Request
from random import randint
from logger import logger

app = FastAPI()

@app.get("/random")
def get_random(request: Request):
    logger.info(f"[service3] Received request: {request.url}")
    value = randint(1, 6)
    logger.info(f"[service3] Generated random value: {value}")
    return {"service": "service3", "random_value": value}
