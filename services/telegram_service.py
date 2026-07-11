import os
import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")


def send_telegram_message(message):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token:
        raise RuntimeError("找不到 TELEGRAM_BOT_TOKEN")

    if not chat_id:
        raise RuntimeError("找不到 TELEGRAM_CHAT_ID")

    response = requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": str(message)[:4000],
        },
        timeout=20,
    )

    print(
        f"TELEGRAM HTTP={response.status_code} RESPONSE={response.text}",
        flush=True,
    )

    response.raise_for_status()
    return True
