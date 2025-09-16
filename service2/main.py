

from fastapi import FastAPI, HTTPException, Request
import requests
from logger import logger

app = FastAPI()

@app.get("/job")
def do_job(request: Request):
    logger.info(f"[service2] Received request: {request.url}")
    try:
        resp = requests.get("http://localhost:8003/random")
        data = resp.json()
        logger.info(f"[service2] Received response from service3: {data}")
        doubled = data["random_value"] * 2
        logger.info(f"[service2] Returning doubled value: {doubled}")
        return {"service": "service2", "original": data["random_value"], "doubled": doubled}
    except Exception as e:
        logger.error(f"[service2] Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
