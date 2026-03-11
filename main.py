from fastapi import FastAPI, Query, Request
from fastapi.responses import PlainTextResponse
from dotenv import load_dotenv
import os

load_dotenv()  # carrega .env da pasta atual (ou do cwd)

app = FastAPI()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/webhooks/whatsapp")
def verify_webhook(
    hub_mode: str = Query(..., alias="hub.mode"),
    hub_challenge: str = Query(..., alias="hub.challenge"),
    hub_verify_token: str = Query(..., alias="hub.verify_token"),
):
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return PlainTextResponse(hub_challenge, status_code=200)
    return PlainTextResponse("verification failed", status_code=403)

@app.post("/webhooks/whatsapp")
async def receive_webhook(request: Request):
    payload = await request.json()
    return {"ok": True}
