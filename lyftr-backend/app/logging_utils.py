import json, time, uuid, datetime

def log_request(request, status, start):
    log = {
        "ts": datetime.datetime.utcnow().isoformat() + "Z",
        "level": "INFO",
        "request_id": str(uuid.uuid4()),
        "method": request.method,
        "path": request.url.path,
        "status": status,
        "latency_ms": int((time.time() - start) * 1000)
    }
    print(json.dumps(log))
