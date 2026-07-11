import os
import requests
from dotenv import load_dotenv

load_dotenv()

LINE_URL = "https://api.line.me/v2/bot/message/broadcast"


def _get_token():
    token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
    if not token:
        raise RuntimeError("找不到 LINE_CHANNEL_ACCESS_TOKEN")
    return token


def _send(messages):
    if os.getenv("DISABLE_LINE_PUSH") == "1":
        print("🔕 LINE 推播已暫停", flush=True)
        return False

    response = requests.post(
        LINE_URL,
        headers={
            "Authorization": f"Bearer {_get_token()}",
            "Content-Type": "application/json",
        },
        json={"messages": messages},
        timeout=20,
    )

    print(
        f"LINE HTTP={response.status_code} RESPONSE={response.text}",
        flush=True,
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"LINE 推播失敗：HTTP {response.status_code}｜{response.text}"
        )

    print("✅ LINE 推播成功", flush=True)
    return True


def send_line_message(message):
    return _send([
        {
            "type": "text",
            "text": str(message)[:4900],
        }
    ])


def send_line_image(image_url):
    return _send([
        {
            "type": "image",
            "originalContentUrl": image_url,
            "previewImageUrl": image_url,
        }
    ])
