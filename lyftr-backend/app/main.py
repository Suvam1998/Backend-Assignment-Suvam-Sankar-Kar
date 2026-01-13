from fastapi import FastAPI, Request, HTTPException
from app.config import WEBHOOK_SECRET
from app.storage import insert_message
from app.models import init_db
from app.metrics import webhook_counter
from app.logging_utils import log_request
import json, re, datetime, hmac, hashlib

app = FastAPI()

@app.on_event("startup")
def startup():
    init_db()

@app.post("/webhook")
async def webhook(req: Request):
    body = await req.body()
    sig = req.headers.get("X-Signature")

    if not sig or not hmac.compare_digest(
        hmac.new(WEBHOOK_SECRET.encode(), body, hashlib.sha256).hexdigest(),
        sig
    ):
        webhook_counter.labels(result="invalid_signature").inc()
        raise HTTPException(401, "invalid signature")

    data = json.loads(body)

    # Validation
    if not re.match(r"^\+\d+$", data["from"]):
        webhook_counter.labels(result="validation_error").inc()
        raise HTTPException(422)

    result = insert_message(data)
    webhook_counter.labels(result=result).inc()

    return {"status": "ok"}
