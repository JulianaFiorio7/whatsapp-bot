from fastapi import FastAPI, Request
import os

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/webhooks/whatsapp")
def verify_webhook(
    hub_mode: str | None = None,
    hub_challenge: str | None = None,
    hub_verify_token: str | None = None,
):
    verify_token = os.getenv("VERIFY_TOKEN", "")
    if hub_mode == "subscribe" and hub_verify_token == verify_token:
        return int(hub_challenge)
    return {"error": "verification failed"}

@app.post("/webhooks/whatsapp")
async def receive_webhook(request: Request):
    payload = await request.json()
    return {"ok": True, "received_keys": list(payload.keys())}
