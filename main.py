from fastapi import FastAPI, Query, Request
from fastapi.responses import PlainTextResponse
import os

app = FastAPI()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/webhooks/whatsapp")
def verify_webhook(
    hub_mode: str = Query(..., alias="hub.mode"),
    hub_challenge: str = Query(..., alias="hub.challenge"),
    hub_verify_token: str = Query(..., alias="hub.verify_token")
):
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return PlainTextResponse(hub_challenge, status_code=200)
    else:
        return PlainTextResponse("verification failed", status_code=403)

@app.post("/webhooks/whatsapp")
async def webhook(request: Request):
    try:
        data = await request.json()
        return {"ok": True, "received_keys": list(data.keys()) if isinstance(data, dict) else []}
    except:
        return {"ok": True}
