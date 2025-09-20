


from fastapi import FastAPI, HTTPException, Request
import requests
from logger import logger
import sqlite3
import os
from opentelemetry.instrumentation.sqlite3 import SQLite3Instrumentor
from opentelemetry import trace

SQLite3Instrumentor().instrument()

tracer = trace.get_tracer("fastapi-service-2")

DB_PATH = "service2_results.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        original INTEGER,
        doubled INTEGER
    )''')
    conn.commit()
    conn.close()

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/job")
def do_job(request: Request):
    with tracer.start_as_current_span("starting_job"):
        logger.info(f"[service2] Received request: {request.url}")
    try:
        with tracer.start_as_current_span("send_request_to_service3"):
            resp = requests.get("http://service3:8003/random")
            
        with tracer.start_as_current_span("validate_data"):
            data = resp.json()
            logger.info(f"[service2] Received response from service3: {data}")
            doubled = data["random_value"] * 2
        # Save to SQLite
        
        with tracer.start_as_current_span("saving_to_db"):
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("INSERT INTO results (original, doubled) VALUES (?, ?)", (data["random_value"], doubled))
            conn.commit()
            conn.close()
            logger.info(f"[service2] Saved to DB: original={data['random_value']}, doubled={doubled}")
            logger.info(f"[service2] Returning doubled value: {doubled}")
            return {"service": "service2", "original": data["random_value"], "doubled": doubled}
    except Exception as e:
        logger.error(f"[service2] Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
